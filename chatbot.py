from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from config import (
    MAX_HISTORY_TURNS,
    MAX_TOKENS,
    MODEL,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    SYSTEM_PROMPT,
)

class Chatbot:
    def __init__(self):
        client_kwargs = {"api_key": OPENAI_API_KEY}
        if OPENAI_BASE_URL:
            client_kwargs["base_url"] = OPENAI_BASE_URL
        self.client = OpenAI(**client_kwargs)
        self.history = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def _trim_history(self):
        """超过最大轮数时，删除最早的对话（保留成对的 user/assistant）"""
        max_messages = MAX_HISTORY_TURNS * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})
        self._trim_history()

        full_reply = ""

        try:
            # 兼容性优先：许多“OpenAI 兼容网关”只实现了 /chat/completions，
            # 但未完整实现 /responses 的事件流协议。
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + list(self.history)
            stream = self.client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True,
                max_tokens=MAX_TOKENS,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    print(delta, end="", flush=True)
                    full_reply += delta
                usage = getattr(chunk, "usage", None)
                if usage:
                    self.total_input_tokens += int(getattr(usage, "prompt_tokens", 0) or 0)
                    self.total_output_tokens += int(getattr(usage, "completion_tokens", 0) or 0)

        except APIConnectionError:
            full_reply = "[错误] 网络连接失败，请检查网络"
        except RateLimitError:
            full_reply = "[错误] 请求太频繁，稍等一下再试"
        except APIStatusError as e:
            msg = getattr(e, "message", "") or str(e)
            full_reply = f"[错误] API 返回异常：HTTP {e.status_code} {msg}".strip()
        except Exception as e:
            full_reply = f"[错误] 未知异常：{type(e).__name__}: {e}"

        if full_reply and not full_reply.startswith("[错误]"):
            self.history.append({"role": "assistant", "content": full_reply})

        return full_reply

    def get_stats(self) -> str:
        return (
            f"对话轮数：{len(self.history) // 2} | "
            f"累计 token：输入 {self.total_input_tokens} / 输出 {self.total_output_tokens}"
        )

    def reset(self):
        self.history = []
        print("对话已重置\n")
