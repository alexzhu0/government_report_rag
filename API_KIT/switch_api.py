#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API提供商切换脚本
快速在DeepSeek和硅基流动API之间切换
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def switch_api_provider(provider: str):
    """
    切换API提供商
    
    Args:
        provider: "deepseek" 或 "siliconflow"
    """
    config_file = project_root / "config" / "config.py"
    
    # 读取配置文件
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新API提供商
    if provider == "deepseek":
        new_content = content.replace(
            'API_PROVIDER = "siliconflow"',
            'API_PROVIDER = "deepseek"'
        )
    elif provider == "siliconflow":
        new_content = content.replace(
            'API_PROVIDER = "deepseek"',
            'API_PROVIDER = "siliconflow"'
        )
    else:
        print(f"❌ 不支持的提供商: {provider}")
        print("支持的提供商: deepseek, siliconflow")
        return False
    
    # 写入更新后的配置
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ API提供商已切换到: {provider}")
    print("请重启API服务以应用更改")
    return True

def show_current_provider():
    """显示当前API提供商"""
    try:
        from config.config import API_PROVIDER
        print(f"当前API提供商: {API_PROVIDER}")
        return API_PROVIDER
    except ImportError as e:
        print(f"❌ 读取配置失败: {e}")
        return None

def main():
    """主函数"""
    print("🔄 API提供商切换工具")
    print("=" * 30)
    
    # 显示当前提供商
    current = show_current_provider()
    
    print("\n可用的API提供商:")
    print("1. deepseek - DeepSeek官方API (推荐)")
    print("2. siliconflow - 硅基流动API")
    
    if len(sys.argv) > 1:
        # 命令行参数
        provider = sys.argv[1].lower()
    else:
        # 交互式选择
        print(f"\n当前使用: {current}")
        choice = input("请选择API提供商 (deepseek/siliconflow): ").strip().lower()
        provider = choice
    
    if provider in ["1", "deepseek"]:
        switch_api_provider("deepseek")
    elif provider in ["2", "siliconflow"]:
        switch_api_provider("siliconflow")
    else:
        print("❌ 无效选择")
        print("使用方法: python switch_api.py [deepseek|siliconflow]")

if __name__ == "__main__":
    main()