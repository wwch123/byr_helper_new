from zhipuai import ZhipuAI

zhipuai_API_KEY='a1c585c7b8106e12b92ceae99026a2cd.frA1fHlR0O4lyba4'
acquirement='''
你的任务是根据用户输入分析用户需求，
如果你觉得用户需要保研信息，返回且仅返回postgraduate，
如果你觉得用户需要实习或者兼职信息，返回且仅返回internship，
如果你无法分类，请返回ERROR
不允许返回除了postgraduate、internship、ERROR以外的回复
'''


def get_classification(user_input):
    user_input=user_input
    if user_input=='':print('输入为空，请重新输入')
    else:
        client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": acquirement+user_input}
            ],
            max_tokens=10
        )

    return response.choices[0].message.content


def test():
    text1='我目前是大三，专业是计算机，请问你有没有导师推荐？'
    text1_1='我目前是大三，专业是计算机，想要保研，请问你有没有导师推荐？'
    text1_2='有没有导师推荐？'
    text2='我想进阿里，有没有阿里的内推消息'
    text2_1='我暑假打算实习，有没有阿里的内推消息'
    text2_2='字节最近在招人嘛？'
    text3='帮我修改代码'
    c=get_classification(text1)
    print(c)
    c=get_classification(text1_1)
    print(c)
    c=get_classification(text1_2)
    print(c)
    c=get_classification(text2)
    print(c)
    c=get_classification(text2_1)
    print(c)
    c=get_classification(text2_2)
    print(c)
    c=get_classification(text3)
    print(c)