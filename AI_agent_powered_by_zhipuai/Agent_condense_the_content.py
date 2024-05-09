from zhipuai import ZhipuAI

def get_condensed_content(user_input,zhipuai_API_KEY):
    user_input=user_input
    if user_input=='':print('输入为空，请重新输入')
    else:
        client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": '帮我浓缩提炼内容，要求保留关键内容，不提炼发信人等次要信息'+user_input}
            ],
        )
    return response.choices[0].message.content