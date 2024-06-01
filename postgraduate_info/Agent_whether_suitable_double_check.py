from zhipuai import ZhipuAI


zhipuai_API_KEY='78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy'#hhz新API key 有效期到2024.6.10

acquirement='''
学生保研需求：{stu_info} ，
老师保研招生信息：{info}，
你是一个拥有行业知识以及科研前沿方向知识的导师，专门帮学生判断学生的需求和老师的招生信息是否匹配
你要帮我严格匹配学生的保研专业需求和老师招生信息是否严格匹配
你要帮我严格匹配学生的保研学位需求和老师招生信息是否严格匹配
如果严格匹配返回且仅返回YES，反之返回且仅返回NO。
'''

def whether_suitable(user_input,condensed_postgraduate_info,zhipuai_API_KEY=zhipuai_API_KEY):
    if user_input=='':
        print('输入为空，请重新输入')
    else:
        client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": acquirement.format(stu_info=user_input,info=condensed_postgraduate_info)}
            ],
            max_tokens=5
        )
    return response.choices[0].message.content
