import streamlit as st
from zhipuai import ZhipuAI
from database.user_history import get_history, add_history, delete_history

# 假设您有以下函数实现在其他模块中：
# get_answer(question) - 根据用户问题返回智能助手的答案
# get_paper(requirements) - 根据用户需求返回生成的论文
# get_history(search_query=None) - 返回历史问答记录

def main():
    st.title("💬 邮邮助手")
    st.caption("🚀 一款北邮学生出品的校园人工智能助手")

    # 页面模式控制
    if 'mode' not in st.session_state:
        st.session_state.mode = 'qa'  # 默认问答模式

    # 侧边栏控制区域
    with st.sidebar:
        st.button("问答助手", on_click=set_mode, args=('qa',))
        st.button("论文助手", on_click=set_mode, args=('paper',))
        st.subheader("历史问答记录")
        search_query = st.text_input("搜索历史记录", key="search_history")
        if st.button("搜索历史记录"):
            history = get_history(search_query)
        else:
            history = get_history()
        for q, a in history:
            with st.expander(f"问：{q}"):
                st.write(f"答：{a}")

    # 主内容区域
    if st.session_state.mode == 'qa':
        # 问答助手模式
        question = st.chat_input("输入您的问题并按回车发送")
        if question:
            answer = get_answer(question, "您的API密钥")
            st.write(f"问：{question}")
            st.write(f"答：{answer}")
            add_history(question, answer)
    elif st.session_state.mode == 'paper':
        # 论文助手模式
        requirements = st.text_input("输入您的论文要求并按回车发送")
        if requirements:
            paper = get_paper(requirements)
            st.write(f"论文内容：{paper}")

def set_mode(mode):
    st.session_state.mode = mode

if __name__ == '__main__':
    main()
