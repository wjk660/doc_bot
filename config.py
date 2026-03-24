import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("缺少 OPENAI_API_KEY（或 ANTHROPIC_API_KEY），请检查 .env 文件")

# Optional: 用于代理或兼容 OpenAI API 的网关
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or os.getenv("ANTHROPIC_BASE_URL")

# 可在 .env 中用 OPENAI_MODEL 覆盖
MODEL = os.getenv("OPENAI_MODEL") or os.getenv("ANTHROPIC_MODEL") or "gpt-4o-mini"
MAX_TOKENS = 1024
MAX_HISTORY_TURNS = 10  # 最多保留最近 10 轮对话

SYSTEM_PROMPT = """你是一个专业的后端开发助手，擅长 Python、数据库和系统设计。
回答要简洁、准确，代码示例用 Python。"""
