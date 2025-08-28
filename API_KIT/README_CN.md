# 🌐 政府工作报告RAG系统 API 服务

## 📋 概述

API_KIT 是政府工作报告RAG系统的RESTful API服务模块，提供标准化的HTTP接口，支持前端应用、自动化工具和第三方系统集成。

### 🎯 主要功能
- **智能查询接口**: 支持自然语言查询政府工作报告
- **系统状态监控**: 实时获取系统运行状态
- **系统初始化**: 远程初始化和重建索引
- **健康检查**: 服务可用性检测
- **跨域支持**: 支持前端应用调用
- **内网穿透**: 集成ngrok支持外网访问

## ⚡ 最新性能优化 v2.1.0

### 🚀 响应速度大幅提升

系统现已完成重大性能优化，API响应速度提升3-5倍：

#### 🔄 多API提供商支持
- **DeepSeek官方API**: 响应更快、稳定性更佳，已修复兼容性问题（推荐）
- **硅基流动API**: 原有提供商，已优化参数配置
- **智能切换**: 一键切换API提供商，无需重新配置系统

#### ⚡ 并发处理优化
- **并发请求**: 支持5-8个并发请求处理
- **批量优化**: 批量查询处理速度提升4倍
- **智能缓存**: 24小时TTL缓存，相同查询毫秒级响应

#### 🎯 向量检索加速
- **GPU搜索**: 向量检索速度提升2-3倍
- **智能索引**: 根据数据规模自动选择最优FAISS索引
- **参数调优**: 动态调整搜索参数，平衡速度和准确性

### 📊 性能提升对比

| 优化项目 | v2.0 性能 | v2.1 性能 | 提升幅度 |
|---------|-----------|-----------|----------|
| 单次查询响应时间 | ~68秒 | 15-25秒 | 3-4倍提升 ⚡ |
| 缓存命中响应时间 | N/A | <100毫秒 | 毫秒级响应 💨 |
| 并发处理能力 | 串行 | 5-8并发 | 4-5倍提升 🚀 |
| 向量检索速度 | 基础 | GPU加速 | 2-3倍提升 ⚡ |

### 🔧 快速启用优化功能

#### 1. API提供商切换
```bash
# 切换到DeepSeek官方API（推荐，已修复兼容性）
python switch_api.py deepseek

# 或切换回硅基流动API
python switch_api.py siliconflow

# 交互式选择
python switch_api.py
```

#### 2. 重启服务体验优化
```bash
start_all.bat  # 重启服务以应用优化
```

#### 3. 性能监控
查看日志中的优化效果标识：
- `⚡ 使用并发执行` - 并发处理启用
- `✅ 从缓存获取查询结果` - 缓存命中
- `🚀 使用GPU加速搜索` - GPU加速启用
- `🔄 使用DeepSeek官方API客户端` - API提供商切换

### 📋 API提供商配置

**DeepSeek官方API配置（推荐）**
```json
{
  "api_key": "sk-6617537f09584c38b63477294794c0d0",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat",
  "timeout": 60,
  "max_concurrent_requests": 8
}
```

**硅基流动API配置（已优化）**
```json
{
  "api_key": "sk-wzkjkykhseibcborkdhvzrqvezrwohvlkdywxgxd",
  "base_url": "https://api.siliconflow.cn/v1", 
  "model": "deepseek-ai/DeepSeek-V3.1",
  "timeout": 120,
  "max_concurrent_requests": 8
}
```

## 🏗️ 架构组件

```
API_KIT/
├── api_server.py           # FastAPI服务器主程序
├── api_models.py           # Pydantic数据模型定义
├── requirements_api.txt    # API服务依赖（已更新，包含openai）
├── switch_api.py          # API提供商切换工具（新增）
├── start_all.bat          # 一键启动脚本（API+ngrok）（已优化）
├── start_api.bat          # API服务启动脚本
├── start_ngrok.bat        # ngrok内网穿透启动脚本
├── ngrok-v3-stable-windows-amd64/  # 内网穿透工具
│   └── ngrok.exe
└── README.md              # 本文档
```

## 🚀 快速启动

### 环境要求
- **Python 3.10+**
- **Conda环境**: 建议使用名为`GovRag`的conda环境
- **依赖包**: 已安装主系统和API服务依赖

### 1. 环境准备
```bash
# 创建并激活conda环境
conda create -n GovRag python=3.10
conda activate GovRag

# 安装主系统依赖
pip install -r ../requirements.txt

# 安装API服务依赖
pip install -r requirements_api.txt
```

### 2. 启动方式

#### 方式1: 一键启动（推荐）
```bash
# Windows用户 - 一键启动API服务和ngrok
start_all.bat
```

此脚本会自动：
1. 启动API服务器（后台运行）
2. 等待15秒让服务器启动
3. 调用系统初始化API
4. 启动ngrok内网穿透

#### 方式2: 单独启动API服务
```bash
# Windows用户
start_api.bat

# 或手动启动
conda activate GovRag
cd ..
uvicorn API_KIT.api_server:app --host 0.0.0.0 --port 8000 --reload
```

#### 方式3: 生产环境启动
```bash
conda activate GovRag
cd ..
uvicorn API_KIT.api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. 访问API文档
启动后访问以下地址：
- **API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **OpenAPI规范**: http://localhost:8000/openapi.json

## 📡 API接口文档

### 1. 智能查询接口
**POST** `/api/query`

查询政府工作报告内容，支持智能分析和多种查询类型。

#### 请求参数
```json
{
  "query": "河南省2025年重点工作有哪些"
}
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "content": "河南省2025年重点工作包括：\n1. 经济发展：GDP增长目标6.5%...",
    "provinces": ["河南"],
    "query_type": "single_province",
    "output_format": "detailed",
    "processing_time": 2.34,
    "processing_stats": {
      "success_rate": 1.0,
      "total_batches": 1,
      "successful_batches": 1
    }
  },
  "message": "查询成功"
}
```

#### 智能查询类型
系统会自动识别查询类型并采用相应的检索策略：

- **单省份查询**: "河南省的经济发展重点"
  - 检索策略：深度检索单个省份（30个块）
  - 输出格式：详细分析报告

- **多省份查询**: "对比广东和江苏的产业发展"
  - 检索策略：多省份平衡检索（每省15个块）
  - 输出格式：对比分析表格

- **全省份查询**: "各省GDP增长目标"
  - 检索策略：全局主题检索
  - 输出格式：省份列表汇总

- **统计查询**: "统计各省投资计划"
  - 检索策略：统计分析检索
  - 输出格式：统计汇总信息

#### 系统优化特性
- **智能分层检索**: 根据查询类型自动选择最优检索策略
- **相邻块聚合**: 确保上下文连续性和完整性
- **上下文窗口最大化**: 支持最大100,000字符的上下文
- **智能截断**: 保留高价值信息，优化输出长度

### 2. 系统状态接口
**GET** `/api/status`

获取系统运行状态和详细统计信息。

#### 响应示例
```json
{
  "success": true,
  "data": {
    "is_ready": true,
    "vector_store_built": true,
    "api_available": true,
    "vector_stats": {
      "total_chunks": 855,
      "total_provinces": 31,
      "index_size": "245MB",
      "embedding_dimension": 1024
    }
  }
}
```

### 3. 系统初始化接口
**POST** `/api/setup`

初始化系统或重建向量索引。

#### 请求参数
```json
{
  "force_rebuild": false
}
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "is_ready": true,
    "vector_store_built": true,
    "api_available": true,
    "vector_stats": {
      "total_chunks": 855,
      "total_provinces": 31
    }
  }
}
```

### 4. 健康检查接口
**GET** `/api/health`

检查API服务是否正常运行。

#### 响应示例
```json
{
  "status": "ok"
}
```

## 🔧 配置说明

### 服务器配置
```python
# api_server.py 中的配置
app = FastAPI(
    title="政府工作报告RAG API",
    description="为AI前端和自动化工具提供标准化接口",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 允许所有来源
    allow_credentials=True,       # 允许凭据
    allow_methods=["*"],          # 允许所有方法
    allow_headers=["*"],          # 允许所有头部
)
```

### 端口配置
- **默认端口**: 8000
- **开发环境**: 支持热重载 (`--reload`)
- **生产环境**: 多进程部署 (`--workers 4`)

### Conda环境配置
```bash
# 推荐的conda环境配置
conda create -n GovRag python=3.10
conda activate GovRag

# 安装CUDA支持（如果有GPU）
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# 安装其他依赖
pip install -r requirements_api.txt
pip install -r ../requirements.txt
```

## 🌍 内网穿透 (ngrok)

### 1. 安装ngrok（首次使用）
⚠️ **重要**：由于GitHub文件大小限制，需要手动下载ngrok.exe

请参考：**[INSTALL_NGROK.md](INSTALL_NGROK.md)** 完成ngrok安装配置

### 2. 自动启动ngrok
```bash
# 使用一键启动脚本
start_all.bat

# 或单独启动ngrok
start_ngrok.bat
```

### 2. 手动配置ngrok
```bash
# 进入ngrok目录
cd ngrok-v3-stable-windows-amd64

# 添加authtoken (需要注册ngrok账号)
ngrok.exe authtoken YOUR_AUTHTOKEN

# 启动内网穿透
ngrok.exe http 8000
```

### 3. 获取公网地址
ngrok启动后会显示公网地址，例如：
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

### 4. 外网访问
- **API文档**: https://abc123.ngrok.io/docs
- **查询接口**: https://abc123.ngrok.io/api/query

## 💻 客户端调用示例

### Python客户端
```python
import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def query_government_report(query_text):
    """查询政府工作报告"""
    url = f"{BASE_URL}/api/query"
    payload = {
        "query": query_text
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def check_system_status():
    """检查系统状态"""
    url = f"{BASE_URL}/api/status"
    response = requests.get(url)
    return response.json()

def initialize_system(force_rebuild=False):
    """初始化系统"""
    url = f"{BASE_URL}/api/setup"
    payload = {
        "force_rebuild": force_rebuild
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 检查系统状态
    status = check_system_status()
    print(f"系统状态: {status}")
    
    # 如果系统未就绪，先初始化
    if not status.get("data", {}).get("is_ready", False):
        print("正在初始化系统...")
        init_result = initialize_system()
        print(f"初始化结果: {init_result}")
    
    # 查询示例
    result = query_government_report("河南省2025年重点工作有哪些")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

### JavaScript客户端
```javascript
// 查询政府工作报告
async function queryGovernmentReport(queryText) {
    const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: queryText
        })
    });
    
    return await response.json();
}

// 检查系统状态
async function checkSystemStatus() {
    const response = await fetch('http://localhost:8000/api/status');
    return await response.json();
}

// 初始化系统
async function initializeSystem(forceRebuild = false) {
    const response = await fetch('http://localhost:8000/api/setup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            force_rebuild: forceRebuild
        })
    });
    
    return await response.json();
}

// 使用示例
async function main() {
    try {
        // 检查系统状态
        const status = await checkSystemStatus();
        console.log('系统状态:', status);
        
        // 如果系统未就绪，先初始化
        if (!status.data?.is_ready) {
            console.log('正在初始化系统...');
            const initResult = await initializeSystem();
            console.log('初始化结果:', initResult);
        }
        
        // 执行查询
        const result = await queryGovernmentReport('河南省2025年重点工作有哪些');
        console.log('查询结果:', result);
    } catch (error) {
        console.error('操作失败:', error);
    }
}

main();
```

### cURL示例
```bash
# 检查系统状态
curl -X GET "http://localhost:8000/api/status"

# 初始化系统
curl -X POST "http://localhost:8000/api/setup" \
  -H "Content-Type: application/json" \
  -d '{"force_rebuild": false}'

# 查询接口
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "河南省2025年重点工作有哪些"}'

# 健康检查
curl -X GET "http://localhost:8000/api/health"
```

## 🔒 安全配置

### 1. 生产环境安全
```python
# 建议的生产环境配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 限制来源域名
    allow_credentials=True,
    allow_methods=["GET", "POST"],             # 限制HTTP方法
    allow_headers=["*"],
)
```

### 2. API密钥认证 (可选扩展)
```python
# 添加API密钥中间件
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != "your-secret-key":
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid API key"}
        )
    response = await call_next(request)
    return response
```

### 3. 请求频率限制
```python
# 使用slowapi进行频率限制
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/query")
@limiter.limit("10/minute")  # 每分钟最多10次请求
async def query_api(request: Request, query_request: QueryRequest):
    # ... 查询逻辑
```

## 📊 性能优化

### 1. 服务器优化
```bash
# 生产环境启动配置
uvicorn API_KIT.api_server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --max-requests 1000 \
  --max-requests-jitter 100
```

### 2. 内存管理
- RAG系统采用单例模式，避免重复初始化
- 向量索引在内存中缓存，提高查询速度
- 定期清理GPU内存缓存
- 支持CUDA加速的Jina Embeddings v4模型

### 3. 并发处理
- 支持多进程部署
- 异步处理长时间查询
- 连接池管理数据库连接

### 4. 系统优化特性
- **智能分层检索架构**: 根据查询类型自动选择最优策略
- **上下文窗口最大化**: 支持100,000字符的大上下文处理
- **相邻块聚合**: 确保信息连续性和完整性
- **智能截断策略**: 保留高价值信息，优化输出长度

## 🚨 错误处理

### 常见错误码
- **400**: 请求参数错误
- **401**: 认证失败 (如果启用了API密钥)
- **500**: 服务器内部错误
- **503**: 服务暂时不可用

### 错误响应格式
```json
{
  "success": false,
  "error": "系统未就绪，请先初始化",
  "message": null,
  "data": null
}
```

## 🔧 故障排除

### 1. 服务启动失败
```bash
# 检查端口占用
netstat -ano | findstr :8000

# 检查依赖安装
pip list | grep fastapi

# 检查主系统配置
python -c "from main import GovernmentReportRAG; print('导入成功')"

# 检查conda环境
conda info --envs
conda activate GovRag
```

### 2. 查询返回错误
- 检查系统是否已初始化 (`/api/status`)
- 确认配置文件正确设置
- 检查API密钥是否有效
- 查看服务器日志
- 确认主系统依赖已安装

### 3. 内网穿透问题
- 确认ngrok authtoken已设置
- 检查防火墙设置
- 确认本地服务正常运行
- 检查ngrok配置文件

### 4. 环境问题
```bash
# 检查conda环境
conda list -n GovRag

# 重新创建环境
conda remove -n GovRag --all
conda create -n GovRag python=3.10
conda activate GovRag
pip install -r requirements_api.txt
pip install -r ../requirements.txt
```

## 📝 开发指南

### 1. 添加新接口
```python
@app.post("/api/new-endpoint")
async def new_endpoint(request: NewRequest):
    try:
        # 处理逻辑
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 2. 修改数据模型
```python
# 在api_models.py中添加新模型
class NewRequest(BaseModel):
    parameter: str
    options: Optional[Dict] = None
```

### 3. 中间件开发
```python
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # 请求前处理
    response = await call_next(request)
    # 响应后处理
    return response
```

## 📋 部署清单

### 开发环境
- [ ] 安装Python 3.10+
- [ ] 创建conda环境（GovRag）
- [ ] 安装依赖包
- [ ] 配置config.py
- [ ] 启动API服务
- [ ] 测试接口功能

### 生产环境
- [ ] 配置反向代理 (Nginx)
- [ ] 设置HTTPS证书
- [ ] 配置防火墙规则
- [ ] 设置系统服务
- [ ] 配置日志轮转
- [ ] 设置监控告警

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交变更
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目遵循项目根目录的LICENSE文件。

## 🆘 技术支持

如有问题，请：
1. 查看本README文档
2. 检查API文档 (http://localhost:8000/docs)
3. 查看项目主README
4. 查看 `logs/government_rag.log` 日志文件
5. 参考 `OPTIMIZATION_SUMMARY.md` 优化报告
6. 提交Issue到项目仓库

## 📈 性能指标

### 系统优化成果
- **平均信息量提升**: 100.0%
- **平均检索量提升**: 100.0% 
- **上下文容量提升**: 337.8%
- **API输出能力提升**: 60.0%

### 检索能力提升
- **单省份查询**: 从10个块提升到30个块（+200%）
- **多省份查询**: 从6个块提升到15个块（+150%）
- **对比查询**: 从8个块提升到25个块（+213%）
- **通用检索**: 从20个块提升到60个块（+200%）

---

**最后更新**: 2025年07月
**版本**: 1.0.0
