#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
向量存储管理器
负责文档向量化、存储和检索
"""

import os
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging
import faiss
from tqdm import tqdm

from data_processor import DocumentChunk
from embedding_manager import get_embedding_manager

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """向量存储管理器"""
    
    def __init__(self, store_path: str, embedding_dim: int = 1024):
        """
        初始化向量存储
        
        Args:
            store_path: 存储路径
            embedding_dim: 向量维度
        """
        self.store_path = Path(store_path)
        self.embedding_dim = embedding_dim
        
        # FAISS索引
        self.index = None
        self.chunks = []  # 存储文档块信息
        self.chunk_embeddings = None
        
        # 文件路径
        self.index_file = self.store_path / "faiss_index.bin"
        self.chunks_file = self.store_path / "chunks_metadata.pkl"
        self.embeddings_file = self.store_path / "embeddings.npy"
        
        # 确保目录存在
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🗄️ 向量存储初始化")
        logger.info(f"📁 存储路径: {self.store_path}")
        logger.info(f"📐 向量维度: {embedding_dim}")
    
    def _create_faiss_index(self, dimension: int, num_docs: int = 0) -> faiss.Index:
        """
        创建FAISS索引 - 智能选择最优索引类型
        
        Args:
            dimension: 向量维度
            num_docs: 预期文档数量
            
        Returns:
            faiss.Index: FAISS索引
        """
        # 根据数据规模选择最优索引
        if num_docs < 10000:
            # 小规模数据，使用FlatL2（精确搜索）
            index = faiss.IndexFlatL2(dimension)
            logger.info(f"📊 创建FlatL2索引: 精确搜索，适合{num_docs}个文档")
            
        elif num_docs < 100000:
            # 中等规模数据，使用IVF索引
            nlist = min(max(int(np.sqrt(num_docs)), 100), 4096)  # 聚类中心数
            quantizer = faiss.IndexFlatL2(dimension)
            index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
            logger.info(f"📊 创建IVFFlat索引: {nlist}个聚类中心，适合{num_docs}个文档")
            
        else:
            # 大规模数据，使用IVF+PQ索引（压缩存储）
            nlist = min(int(np.sqrt(num_docs)), 4096)
            m = min(dimension // 8, 64)  # PQ子量化器数量
            quantizer = faiss.IndexFlatL2(dimension) 
            index = faiss.IndexIVFPQ(quantizer, dimension, nlist, m, 8)
            logger.info(f"📊 创建IVFPQ索引: {nlist}个聚类，{m}个PQ，适合{num_docs}个文档")
            
        return index
    
    def build_index(self, chunks: List[DocumentChunk], batch_size: int = 32, embedding_manager=None) -> bool:
        """
        构建向量索引
        
        Args:
            chunks: 文档块列表
            batch_size: 批处理大小
            embedding_manager: embedding管理器实例（可选）
            
        Returns:
            bool: 是否构建成功
        """
        logger.info(f"🔨 开始构建向量索引...")
        logger.info(f"📚 文档块数量: {len(chunks)}")
        
        if not chunks:
            logger.error("❌ 没有文档块可以索引")
            return False
        
        try:
            # 获取embedding管理器 - 使用SDPA优化
            if embedding_manager is None:
                embedding_manager = get_embedding_manager(attn_implementation="sdpa")
            
            if not embedding_manager.is_model_loaded():
                logger.error("❌ Embedding模型未加载")
                return False
            
            # 提取文本内容
            texts = [chunk.content for chunk in chunks]
            
            # 批量编码文本
            logger.info("🔄 正在编码文本...")
            embeddings = embedding_manager.encode_texts(
                texts, 
                batch_size=batch_size, 
                show_progress=True
            )
            
            if len(embeddings) == 0:
                logger.error("❌ 文本编码失败")
                return False
            
            # 更新向量维度
            self.embedding_dim = embeddings.shape[1]
            logger.info(f"📐 实际向量维度: {self.embedding_dim}")
            
            # 创建FAISS索引 - 传入文档数量用于优化
            self.index = self._create_faiss_index(self.embedding_dim, len(chunks))
            
            # 如果使用IVF索引，需要训练
            if hasattr(self.index, 'train'):
                logger.info("🎯 训练IVF索引...")
                self.index.train(embeddings.astype(np.float32))
            
            # 添加向量到索引
            logger.info("📊 添加向量到索引...")
            self.index.add(embeddings.astype(np.float32))
            
            # 保存数据
            self.chunks = chunks
            self.chunk_embeddings = embeddings
            
            logger.info(f"✅ 向量索引构建完成!")
            logger.info(f"📊 索引大小: {self.index.ntotal}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 构建索引失败: {str(e)}")
            return False
    
    def save_index(self) -> bool:
        """
        保存索引到磁盘
        
        Returns:
            bool: 是否保存成功
        """
        try:
            if self.index is None:
                logger.error("❌ 没有可保存的索引")
                return False
            
            logger.info("💾 保存向量索引...")
            
            # 保存FAISS索引
            faiss.write_index(self.index, str(self.index_file))
            
            # 保存文档块元数据
            with open(self.chunks_file, 'wb') as f:
                pickle.dump(self.chunks, f)
            
            # 保存embeddings
            if self.chunk_embeddings is not None:
                np.save(self.embeddings_file, self.chunk_embeddings)
            
            logger.info(f"✅ 索引保存成功!")
            logger.info(f"📄 索引文件: {self.index_file}")
            logger.info(f"📄 元数据文件: {self.chunks_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 保存索引失败: {str(e)}")
            return False
    
    def load_index(self) -> bool:
        """
        从磁盘加载索引
        
        Returns:
            bool: 是否加载成功
        """
        try:
            if not self.index_file.exists():
                logger.warning(f"⚠️ 索引文件不存在: {self.index_file}")
                return False
            
            logger.info("📂 加载向量索引...")
            
            # 加载FAISS索引
            self.index = faiss.read_index(str(self.index_file))
            
            # 加载文档块元数据
            if self.chunks_file.exists():
                with open(self.chunks_file, 'rb') as f:
                    self.chunks = pickle.load(f)
            
            # 加载embeddings
            if self.embeddings_file.exists():
                self.chunk_embeddings = np.load(self.embeddings_file)
            
            # 更新维度信息
            if self.index:
                self.embedding_dim = self.index.d
            
            logger.info(f"✅ 索引加载成功!")
            logger.info(f"📊 索引大小: {self.index.ntotal}")
            logger.info(f"📚 文档块数量: {len(self.chunks)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 加载索引失败: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 10, 
               province_filter: Optional[str] = None,
               chunk_type_filter: Optional[str] = None,
               use_gpu: bool = False) -> List[Tuple[DocumentChunk, float]]:
        """
        搜索相关文档 - GPU加速版本
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            province_filter: 省份过滤
            chunk_type_filter: 块类型过滤
            use_gpu: 是否使用GPU加速搜索
            
        Returns:
            List[Tuple[DocumentChunk, float]]: (文档块, 相似度分数)列表
        """
        if self.index is None:
            logger.error("❌ 索引未加载")
            return []
        
        try:
            # 编码查询文本 - 使用SDPA优化
            embedding_manager = get_embedding_manager(attn_implementation="sdpa")
            query_embedding = embedding_manager.encode_texts([query], show_progress=False)
            
            if len(query_embedding) == 0:
                logger.error("❌ 查询编码失败")
                return []
            
            # GPU加速搜索
            index_to_use = self.index
            if use_gpu and hasattr(faiss, 'StandardGpuResources'):
                try:
                    gpu_res = faiss.StandardGpuResources()
                    index_to_use = faiss.index_cpu_to_gpu(gpu_res, 0, self.index)
                    logger.debug("🚀 使用GPU加速搜索")
                except Exception as e:
                    logger.warning(f"⚠️ GPU搜索失败，使用CPU: {e}")
                    index_to_use = self.index
            
            # 智能确定搜索范围
            search_k = min(max(top_k * 4, 200), index_to_use.ntotal)
            
            # IVF索引需要设置搜索参数
            if hasattr(index_to_use, 'nprobe'):
                # 动态调整nprobe以平衡速度和准确性
                original_nprobe = index_to_use.nprobe
                index_to_use.nprobe = min(max(search_k // 50, 10), 100)
                logger.debug(f"🎯 IVF搜索参数: nprobe={index_to_use.nprobe}")
            
            # 执行搜索
            scores, indices = index_to_use.search(
                query_embedding.astype(np.float32), 
                search_k
            )
            
            # 恢复原始nprobe设置
            if hasattr(index_to_use, 'nprobe'):
                index_to_use.nprobe = original_nprobe
            
            results = []
            
            for score, idx in zip(scores[0], indices[0]):
                if idx >= len(self.chunks) or idx < 0:
                    continue
                
                chunk = self.chunks[idx]
                
                # 应用过滤器
                if province_filter and chunk.province != province_filter:
                    continue
                
                if chunk_type_filter and chunk.chunk_type != chunk_type_filter:
                    continue
                
                # 转换距离为相似度分数 (L2距离转余弦相似度近似)
                similarity = 1.0 / (1.0 + score)
                
                results.append((chunk, similarity))
                
                if len(results) >= top_k:
                    break
            
            logger.debug(f"🔍 搜索完成: 查询='{query[:50]}...', 结果数={len(results)}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ 搜索失败: {str(e)}")
            return []
    
    def get_chunks_by_province(self, province: str) -> List[DocumentChunk]:
        """
        获取指定省份的所有文档块
        
        Args:
            province: 省份名称
            
        Returns:
            List[DocumentChunk]: 文档块列表
        """
        return [chunk for chunk in self.chunks if chunk.province == province]
    
    def get_chunks_by_type(self, chunk_type: str) -> List[DocumentChunk]:
        """
        获取指定类型的所有文档块
        
        Args:
            chunk_type: 块类型
            
        Returns:
            List[DocumentChunk]: 文档块列表
        """
        return [chunk for chunk in self.chunks if chunk.chunk_type == chunk_type]
    
    def get_statistics(self) -> Dict:
        """
        获取索引统计信息
        
        Returns:
            Dict: 统计信息
        """
        if not self.chunks:
            return {}
        
        # 省份统计
        province_stats = {}
        type_stats = {}
        
        for chunk in self.chunks:
            # 省份统计
            province = chunk.province
            if province not in province_stats:
                province_stats[province] = {"count": 0, "total_chars": 0}
            province_stats[province]["count"] += 1
            province_stats[province]["total_chars"] += chunk.char_count
            
            # 类型统计
            chunk_type = chunk.chunk_type
            if chunk_type not in type_stats:
                type_stats[chunk_type] = 0
            type_stats[chunk_type] += 1
        
        return {
            "total_chunks": len(self.chunks),
            "total_provinces": len(province_stats),
            "index_size": self.index.ntotal if self.index else 0,
            "embedding_dimension": self.embedding_dim,
            "province_stats": province_stats,
            "type_stats": type_stats
        }
    
    def is_built(self) -> bool:
        """检查索引是否已构建"""
        return self.index is not None and self.index.ntotal > 0

# 全局向量存储实例
_vector_store = None

def get_vector_store() -> VectorStore:
    """获取全局向量存储实例 - 使用SDPA优化"""
    global _vector_store
    if _vector_store is None:
        from config.config import DATA_PATHS
        
        # 获取embedding维度 - 使用SDPA优化
        embedding_manager = get_embedding_manager(attn_implementation="sdpa")
        embedding_dim = embedding_manager.get_embedding_dimension()
        
        _vector_store = VectorStore(
            store_path=str(DATA_PATHS["vector_store"]),
            embedding_dim=embedding_dim
        )
        
        # 尝试加载已有索引
        _vector_store.load_index()
    
    return _vector_store

 