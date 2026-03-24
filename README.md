# llm_01

一个简单的终端聊天助手示例（OpenAI Python SDK + 流式输出）。

## 运行环境

- macOS / Linux
- Python 3.10+（推荐用项目自带虚拟环境 `.venv`）

## 配置

在项目根目录创建/编辑 `.env`，至少包含：

```bash
OPENAI_API_KEY=sk-xxxxxxxx
```

兼容：如果你已经有 `ANTHROPIC_API_KEY/ANTHROPIC_BASE_URL/ANTHROPIC_MODEL`，也可以不改 `.env`，代码会自动回退读取这些变量来配置 OpenAI SDK（常用于 OpenAI 兼容网关）。

## 启动

首次或日常启动都可以直接执行：

```bash
bash run.sh
```

脚本会：

- 若不存在则创建 `.venv`
- 安装/更新 `requirements.txt` 依赖到 `.venv`
- 使用 `.venv` 的 Python 运行 `main.py`

启动后可用命令：

- `/reset` 重置对话
- `/stats` 查看 token 统计
- `/quit` 退出

## 手动方式（可选）

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```
