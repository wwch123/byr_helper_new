import streamlit as st
from zhipuai import ZhipuAI
from AI_agent_powered_by_zhipuai.Agent_01_classify_questions import get_classification
from AI_agent_powered_by_zhipuai.Agent_02_emotional_companion import get_emotional_support
from AI_agent_powered_by_zhipuai.Agent_03_give_normal_answer import get_normal_answer
from AI_agent_powered_by_zhipuai.Agent_04_memory import store_memory
from AI_agent_powered_by_zhipuai.Agent_05_is_coherent import is_coherent


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
        # 正确的调用
        st.chat_message("How can I help you?")

        # 这里进行问题分类
        category = self.get_classification(prompt)

        # 根据分类调用不同的回答函数
        if category == '保研':
            answer = self.get_graduate_answer(prompt)
        elif category == '实习':
            answer = self.get_internship_answer(prompt)
        elif category == '情感生活':
            answer = self.get_emotional_support(prompt)
        else:
            answer = "对不起，我无法理解您的问题。"

        self.messages.append({"role": "assistant", "content": answer})
        st.chat_message({"role": "assistant", "content": answer})  # 显示助手的回答

    def get_classification(self, user_input):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": background_info},
                {"role": "user", "content": user_input}
            ],
        )
        return response.choices[0].message.content

    # 各种分类问题的回答函数
    def get_graduate_answer(self, user_input):
        # Placeholder: 实际回答函数的实现
        return "关于保研的答案：[详细回答]"

    def get_internship_answer(self, user_input):
        # Placeholder: 实际回答函数的实现
        return "关于实习的答案：[详细回答]"

    def get_emotional_support(self, user_input):
        # Placeholder: 实际回答函数的实现
        return "关于情感生活的支持：[详细回答]"


if __name__ == '__main__':
    qa_app = MyQAApp()
    qa_app.run()
# Placeholder background_info for classification
background_info = '''
# Role
问题分类智能体

## Profile
- Description: 识别并分类用户提出的问题，将其归入预定的类别“保研”、“实习”、“情感生活”中。

## Rules
- 只能返回“保研”、“实习”、“情感生活”这三个类别中的一个。
'''