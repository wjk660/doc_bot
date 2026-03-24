from chatbot import Chatbot

def main():
    bot = Chatbot()
    print("=" * 50)
    print("后端开发助手（输入 /reset 重置，/stats 查看统计，/quit 退出）")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再见！")
            break

        if not user_input:
            continue

        if user_input == "/quit":
            print(f"\n{bot.get_stats()}")
            print("再见！")
            break
        elif user_input == "/reset":
            bot.reset()
            continue
        elif user_input == "/stats":
            print(f"{bot.get_stats()}\n")
            continue

        print("AI: ", end="")
        reply = bot.chat(user_input)
        # 正常情况下 reply 会在 bot.chat() 内部流式打印出来；如果请求失败，确保错误信息可见。
        if reply.startswith("[错误]"):
            print(reply, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()
