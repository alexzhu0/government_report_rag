#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查询缓存管理器
负责缓存查询结果，提升响应速度
"""

import hashlib
import json
import logging
import pickle
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import threading

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    content: str
    provinces: List[str]
    query_type: str
    output_format: str
    processing_time: float
    processing_stats: Dict[str, Any]
    timestamp: float
    hit_count: int = 0
    
    
class QueryCache:
    """查询缓存管理器"""
    
    def __init__(
        self, 
        cache_dir: str, 
        max_entries: int = 1000,
        ttl_hours: int = 24,
        auto_save_interval: int = 300  # 5分钟自动保存
    ):
        """
        初始化查询缓存
        
        Args:
            cache_dir: 缓存目录
            max_entries: 最大缓存条目数
            ttl_hours: 缓存过期时间（小时）
            auto_save_interval: 自动保存间隔（秒）
        """
        self.cache_dir = Path(cache_dir)
        self.max_entries = max_entries
        self.ttl_seconds = ttl_hours * 3600
        self.auto_save_interval = auto_save_interval
        
        # 内存缓存
        self.memory_cache: Dict[str, CacheEntry] = {}
        
        # 线程锁
        self.lock = threading.RLock()
        
        # 缓存文件路径
        self.cache_file = self.cache_dir / "query_cache.pkl"
        self.stats_file = self.cache_dir / "cache_stats.json"
        
        # 缓存统计
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "cache_saves": 0,
            "last_cleanup": time.time()
        }
        
        # 确保目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载缓存
        self._load_cache()
        
        # 启动自动保存线程
        self._start_auto_save_thread()
        
        logger.info(f"💾 查询缓存初始化完成")
        logger.info(f"📁 缓存目录: {self.cache_dir}")
        logger.info(f"📊 最大条目数: {max_entries}")
        logger.info(f"⏰ TTL: {ttl_hours} 小时")
    
    def _generate_cache_key(self, query: str, **kwargs) -> str:
        """生成缓存键"""
        # 包含查询文本和相关参数
        cache_data = {
            "query": query.strip().lower(),
            **kwargs
        }
        
        # 生成MD5哈希
        cache_str = json.dumps(cache_data, sort_keys=True, ensure_ascii=False)
        cache_key = hashlib.md5(cache_str.encode('utf-8')).hexdigest()
        
        return cache_key
    
    def get(self, query: str, **kwargs) -> Optional[CacheEntry]:
        """
        获取缓存结果
        
        Args:
            query: 查询文本
            **kwargs: 其他查询参数
            
        Returns:
            CacheEntry: 缓存条目，如果不存在或过期返回None
        """
        with self.lock:
            self.stats["total_requests"] += 1
            
            cache_key = self._generate_cache_key(query, **kwargs)
            
            if cache_key in self.memory_cache:
                entry = self.memory_cache[cache_key]
                
                # 检查是否过期
                if time.time() - entry.timestamp <= self.ttl_seconds:
                    entry.hit_count += 1
                    self.stats["cache_hits"] += 1
                    logger.debug(f"✅ 缓存命中: {cache_key[:8]}...")
                    return entry
                else:
                    # 过期，删除
                    del self.memory_cache[cache_key]
                    logger.debug(f"⏰ 缓存过期: {cache_key[:8]}...")
            
            self.stats["cache_misses"] += 1
            logger.debug(f"❌ 缓存未命中: {cache_key[:8]}...")
            return None
    
    def put(self, query: str, result: Dict[str, Any], **kwargs):
        """
        保存查询结果到缓存
        
        Args:
            query: 查询文本
            result: 查询结果
            **kwargs: 其他查询参数
        """
        with self.lock:
            cache_key = self._generate_cache_key(query, **kwargs)
            
            entry = CacheEntry(
                key=cache_key,
                content=result.get("content", ""),
                provinces=result.get("provinces", []),
                query_type=result.get("query_type", "unknown"),
                output_format=result.get("output_format", "unknown"),
                processing_time=result.get("processing_time", 0.0),
                processing_stats=result.get("processing_stats", {}),
                timestamp=time.time(),
                hit_count=0
            )
            
            self.memory_cache[cache_key] = entry
            self.stats["cache_saves"] += 1
            
            logger.debug(f"💾 结果已缓存: {cache_key[:8]}...")
            
            # 检查是否需要清理
            if len(self.memory_cache) > self.max_entries:
                self._cleanup_cache()
    
    def _cleanup_cache(self):
        """清理过期和老旧的缓存条目"""
        current_time = time.time()
        
        # 删除过期条目
        expired_keys = [
            key for key, entry in self.memory_cache.items()
            if current_time - entry.timestamp > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self.memory_cache[key]
        
        # 如果仍然超过限制，删除最少使用的条目
        if len(self.memory_cache) > self.max_entries:
            # 按照命中次数和时间戳排序，删除最少使用的
            sorted_entries = sorted(
                self.memory_cache.items(),
                key=lambda x: (x[1].hit_count, x[1].timestamp)
            )
            
            entries_to_remove = len(self.memory_cache) - self.max_entries
            for i in range(entries_to_remove):
                key = sorted_entries[i][0]
                del self.memory_cache[key]
        
        self.stats["last_cleanup"] = current_time
        logger.info(f"🧹 缓存清理完成: 删除{len(expired_keys)}个过期条目")
    
    def _save_cache(self):
        """保存缓存到磁盘"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.memory_cache, f)
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"💾 缓存已保存: {len(self.memory_cache)} 条目")
            
        except Exception as e:
            logger.error(f"❌ 缓存保存失败: {str(e)}")
    
    def _load_cache(self):
        """从磁盘加载缓存"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'rb') as f:
                    self.memory_cache = pickle.load(f)
                
                # 清理过期条目
                self._cleanup_cache()
                
                logger.info(f"📂 缓存加载完成: {len(self.memory_cache)} 条目")
            
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats.update(json.load(f))
                    
        except Exception as e:
            logger.warning(f"⚠️ 缓存加载失败: {str(e)}")
            self.memory_cache = {}
    
    def _start_auto_save_thread(self):
        """启动自动保存线程"""
        def auto_save():
            while True:
                time.sleep(self.auto_save_interval)
                with self.lock:
                    if self.memory_cache:
                        self._save_cache()
        
        import threading
        thread = threading.Thread(target=auto_save, daemon=True)
        thread.start()
        
        logger.info(f"⚡ 自动保存线程已启动: {self.auto_save_interval}秒间隔")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self.lock:
            hit_rate = 0.0
            if self.stats["total_requests"] > 0:
                hit_rate = self.stats["cache_hits"] / self.stats["total_requests"]
            
            return {
                "cache_entries": len(self.memory_cache),
                "max_entries": self.max_entries,
                "total_requests": self.stats["total_requests"],
                "cache_hits": self.stats["cache_hits"],
                "cache_misses": self.stats["cache_misses"],
                "hit_rate": hit_rate,
                "cache_saves": self.stats["cache_saves"],
                "last_cleanup": self.stats["last_cleanup"],
                "ttl_hours": self.ttl_seconds / 3600
            }
    
    def clear_cache(self):
        """清空所有缓存"""
        with self.lock:
            self.memory_cache.clear()
            self.stats = {
                "total_requests": 0,
                "cache_hits": 0,
                "cache_misses": 0,
                "cache_saves": 0,
                "last_cleanup": time.time()
            }
            logger.info("🧹 缓存已清空")
    
    def save_and_close(self):
        """保存缓存并关闭"""
        with self.lock:
            self._save_cache()
            logger.info("💾 缓存已保存并关闭")


# 全局缓存实例
_query_cache = None


def get_query_cache() -> QueryCache:
    """获取全局查询缓存实例"""
    global _query_cache
    if _query_cache is None:
        from config.config import DATA_PATHS
        
        cache_dir = DATA_PATHS.get("vector_store", Path("./data/vectors")) / "cache"
        _query_cache = QueryCache(
            cache_dir=str(cache_dir),
            max_entries=1000,
            ttl_hours=24,
            auto_save_interval=300
        )
    
    return _query_cache