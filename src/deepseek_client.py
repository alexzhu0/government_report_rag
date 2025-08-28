#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DeepSeek官方API客户端
使用直接HTTP请求方式，避免OpenAI SDK版本兼容问题
"""

import logging
import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """API响应数据结构"""
    success: bool
    content: str
    usage: Optional[Dict] = None
    error: Optional[str] = None
    response_time: Optional[float] = None


class DeepSeekClient:
    """DeepSeek官方API客户端 - 使用直接HTTP请求"""

    def __init__(
        self, 
        api_key: str, 
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-chat"
    ):
        """
        初始化DeepSeek API客户端

        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        
        # 创建session以复用连接
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        logger.info("🚀 初始化DeepSeek API客户端")
        logger.info(f"🔗 Base URL: {base_url}")
        logger.info(f"🤖 模型: {model}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 8000,
        timeout: int = 60,
    ) -> APIResponse:
        """
        调用聊天完成API

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            timeout: 请求超时时间

        Returns:
            APIResponse: API响应结果
        """
        start_time = time.time()

        try:
            logger.debug(f"📤 发送请求到DeepSeek API")
            logger.debug(f"📝 消息数量: {len(messages)}")

            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }

            response = self.session.post(url, json=payload, timeout=timeout)
            response_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                usage = result.get("usage", {})

                logger.info(f"✅ DeepSeek API调用成功 ({response_time:.2f}s)")
                logger.debug(f"📊 Token使用: {usage}")

                return APIResponse(
                    success=True,
                    content=content,
                    usage=usage,
                    response_time=response_time,
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ DeepSeek API调用失败: {error_msg}")
                return APIResponse(
                    success=False,
                    content="",
                    error=error_msg,
                    response_time=response_time,
                )

        except requests.exceptions.Timeout:
            error_msg = f"请求超时 ({timeout}s)"
            logger.error(f"⏰ {error_msg}")
            return APIResponse(
                success=False,
                content="",
                error=error_msg,
                response_time=time.time() - start_time,
            )

        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求异常: {str(e)}"
            logger.error(f"🌐 {error_msg}")
            return APIResponse(
                success=False,
                content="",
                error=error_msg,
                response_time=time.time() - start_time,
            )

        except json.JSONDecodeError as e:
            error_msg = f"JSON解析失败: {str(e)}"
            logger.error(f"📄 {error_msg}")
            return APIResponse(
                success=False,
                content="",
                error=error_msg,
                response_time=time.time() - start_time,
            )

        except Exception as e:
            error_msg = f"DeepSeek API调用失败: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return APIResponse(
                success=False,
                content="",
                error=error_msg,
                response_time=time.time() - start_time,
            )

    def simple_chat(
        self, user_message: str, system_message: str = None, **kwargs
    ) -> APIResponse:
        """
        简化的聊天接口

        Args:
            user_message: 用户消息
            system_message: 系统消息（可选）
            **kwargs: 其他参数

        Returns:
            APIResponse: API响应结果
        """
        messages = []

        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": user_message})

        return self.chat_completion(messages, **kwargs)

    def concurrent_batch_process(
        self,
        queries: List[str],
        system_message: str = None,
        max_workers: int = 8,
        timeout_per_request: int = 60,
    ) -> List[APIResponse]:
        """
        并发批量处理查询

        Args:
            queries: 查询列表
            system_message: 系统消息
            max_workers: 最大并发工作线程数
            timeout_per_request: 单个请求超时时间

        Returns:
            List[APIResponse]: 响应列表
        """
        if not queries:
            return []

        logger.info(f"🚀 开始DeepSeek并发批量处理: {len(queries)} 个查询，{max_workers} 个工作线程")
        results = [None] * len(queries)
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_index = {
                executor.submit(
                    self.simple_chat,
                    query,
                    system_message,
                    timeout=timeout_per_request
                ): i
                for i, query in enumerate(queries)
            }

            # 收集结果
            for future in as_completed(future_to_index, timeout=300):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                    
                    status = "✅" if result.success else "❌"
                    logger.debug(f"{status} DeepSeek查询 {index + 1}/{len(queries)} 完成")
                    
                except Exception as e:
                    logger.error(f"❌ DeepSeek查询 {index + 1} 异常: {str(e)}")
                    results[index] = APIResponse(
                        success=False,
                        content="",
                        error=str(e)
                    )

        # 处理未完成的任务
        for i, result in enumerate(results):
            if result is None:
                results[i] = APIResponse(
                    success=False,
                    content="",
                    error="任务超时或未完成"
                )

        processing_time = time.time() - start_time
        success_count = sum(1 for r in results if r.success)
        
        logger.info(f"📊 DeepSeek并发批量处理完成: {success_count}/{len(queries)} 成功 ({processing_time:.2f}s)")
        logger.info(f"⚡ 平均速度: {processing_time / len(queries):.2f}s/查询")

        return results

    def test_connection(self) -> bool:
        """
        测试DeepSeek API连接

        Returns:
            bool: 连接是否成功
        """
        logger.info("🔍 测试DeepSeek API连接...")

        response = self.simple_chat("你好，请回复'连接成功'", max_tokens=50, timeout=30)

        if response.success:
            logger.info("✅ DeepSeek API连接测试成功")
            return True
        else:
            logger.error(f"❌ DeepSeek API连接测试失败: {response.error}")
            return False


# 全局DeepSeek客户端实例
_deepseek_client = None


def get_deepseek_client() -> DeepSeekClient:
    """获取全局DeepSeek客户端实例"""
    global _deepseek_client
    if _deepseek_client is None:
        from config.config import DEEPSEEK_CONFIG

        _deepseek_client = DeepSeekClient(
            api_key=DEEPSEEK_CONFIG["api_key"],
            base_url=DEEPSEEK_CONFIG["base_url"],
            model=DEEPSEEK_CONFIG["model"],
        )
    return _deepseek_client