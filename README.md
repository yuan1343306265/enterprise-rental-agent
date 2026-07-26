# 企业级租房顾问 Agent
![自动化测试](https://github.com/yuan1343306265/enterprise-rental-agent/actions/workflows/tests.yml/badge.svg)](https://github.com/yuan1343306265/enterprise-rental-agent/actions/workflows/tests.yml)

一个基于 FastAPI、LangChain、DeepSeek 和 SQLAlchemy 构建的租房顾问 Agent。

用户可以使用自然语言描述预算、区域、户型、宠物和通勤时间等需求，Agent 会调用房源查询工具进行检索，并通过 `session_id` 保存和恢复多轮对话。

## 核心功能

- 自然语言租房咨询
- 大模型工具调用
- 房源数据库查询
- 基于 `session_id` 的多轮对话记忆
- 异步数据库操作
- 请求超时与失败重试
- Agent 并发数量限制
- 工具调用次数限制
- 结构化日志与异常处理
- FastAPI 接口文档
- pytest 自动化测试
- GitHub Actions 持续集成
- Docker 容器化配置

## 技术栈

| 分类 | 技术 |
| --- | --- |
| Web 框架 | FastAPI、Uvicorn |
| Agent 框架 | LangChain |
| 大语言模型 | DeepSeek |
| 数据库 | SQLite、SQLAlchemy Async |
| 数据校验 | Pydantic |
| 自动化测试 | pytest、FastAPI TestClient |
| 持续集成 | GitHub Actions |
| 容器化 | Docker |

## 项目结构

```text
rental_agent/
├─ app/
│  ├─ agent/                 # Agent、提示词、模型和工具
│  ├─ database/              # 数据库连接和 ORM 模型
│  ├─ schemas/               # Pydantic 请求与响应模型
│  ├─ services/              # 对话记录和房源业务逻辑
│  ├─ config.py              # 环境配置
│  ├─ logging_config.py      # 日志配置
│  └─ main.py                # FastAPI 应用入口
├─ tests/                    # 自动化测试
├─ .github/workflows/        # GitHub Actions 配置
├─ Dockerfile                # Docker 镜像配置
├─ requirements.txt          # Python 依赖
└─ README.md                 # 项目说明

## 本地运行

### 1. 下载项目

```powershell
git clone https://github.com/yuan1343306265/enterprise-rental-agent.git
cd enterprise-rental-agent
```

### 2. 安装依赖

```powershell
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量示例文件：

```powershell
Copy-Item .env.example .env
```

打开 `.env`，填写自己的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=你的密钥
```

### 4. 启动服务

```powershell
uvicorn app.main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```


## API 接口

### 健康检查

```http
GET /api/health
```

用于检查服务是否正常运行。

### 租房咨询

```http
POST /api/chat
```

请求示例：

```json
{
  "message": "我预算5000元，想在朝阳租一居室，可以养猫，通勤不超过40分钟。",
  "session_id": "demo-session-1"
}
```

使用相同的 `session_id` 再次提问时，Agent 会读取之前的聊天记录。

### 查询会话历史

```http
GET /api/sessions/{session_id}
```

示例：

```text
GET /api/sessions/demo-session-1
```

## 自动化测试

在项目根目录执行：

```powershell
python -m pytest -v
```

当前测试覆盖：

- 健康检查接口
- 租房咨询接口
- 无效请求的数据校验

代码上传到 GitHub 后，GitHub Actions 会自动安装依赖并运行全部测试。

## Docker

电脑安装并启动 Docker 后，在项目根目录构建镜像：

```powershell
docker build -t enterprise-rental-agent .
```

启动容器：

```powershell
docker run --env-file .env -p 8000:8000 enterprise-rental-agent
```

然后访问：

```text
http://127.0.0.1:8000/docs
```

> 当前仓库已提供 `Dockerfile` 和 `.dockerignore`；Docker 命令需要先安装 Docker Desktop。



## Agent 执行流程

1. FastAPI 接收用户问题和 `session_id`。
2. 根据 `session_id` 从数据库读取最近的聊天记录。
3. 将历史消息和当前问题发送给 DeepSeek。
4. 模型判断是否需要调用房源查询工具。
5. 工具根据预算、区域、户型、宠物和通勤条件查询数据库。
6. 将工具查询结果重新交给模型生成最终回答。
7. 把用户问题和 Agent 回答保存到数据库。
8. 返回结构化 API 响应。

为了提高稳定性，接口还增加了超时控制、失败重试、并发限制和工具调用次数限制。