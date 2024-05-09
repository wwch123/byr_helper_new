import streamlit as st
from zhipuai import ZhipuAI


class MyQAApp:
    def __init__(self):
        # 使用内置的开发者API
        self.api_key = "50ea3c031b07edc77a6a640ccb1526d1.NUhtei288b3OrwF4"
        self.client = ZhipuAI(api_key=self.api_key)
        self.response = None
        self.messages = []

    def run(self):
        st.title("💬 邮邮助手")
        st.caption("🚀 一款北邮学生出品的校园人工智能助手")

        # 不再需要用户输入API
        self.display_info()

        if not self.messages:
            self.messages.append({"role": "assistant", "content": "How can I help you?"})
            st.chat_message({"role": "assistant", "content": "How can I help you?"})

        if prompt := st.chat_input():
            self.ask_question(prompt)

    def display_info(self):
        with st.sidebar:
            st.markdown("🔑 Using internal developer API")
            st.markdown("[View the source code](https://github.com/your/repository)")
            st.markdown(
                "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/your/repository?quickstart=1)")

    def ask_question(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        st.chat_message({"role": "user", "content": prompt})  # 显示用户的问题

        self.response = self.client.chat.completions.create(
            model="glm-4v",
            messages=self.messages,
            stream=True,
            tools=[
                {
                    "type": "retrieval",
                    "retrieval": {
                        "knowledge_id": "1765660633795276800",
                        "prompt_template": "如果用户问文档中的相关问题就直接回答。不是文档里的相关内容你就告诉用户我不太清楚，或者让用户再问的具体一点。不要复述问题，直接开始回答。"
                    }
                }
            ],
        )

        # 从response中读取回答
        msg = ""
        for chunk in self.response:
            msg += chunk.choices[0].delta.content

        self.messages.append({"role": "assistant", "content": msg})
        st.chat_message({"role": "assistant", "content": msg})  # 显示助手的回答

###aaaaa
if __name__ == '__main__':
    qa_app = MyQAApp()
    qa_app.run()
