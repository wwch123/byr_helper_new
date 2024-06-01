from zhipuai import ZhipuAI

zhipuai_API_KEY='78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy' # 替换为你的API key，有效期到2024.6.10

acquirement='''
学生实习需求：{stu_info}，
公司实习岗位信息：{info}，
你是一个拥有行业知识以及职位要求知识的导师，专门帮学生判断学生的需求和公司实习岗位信息是否匹配
你要从以下几个方面帮我分析是否匹配：
1. 公司的企业文化和学生的个人价值观是否匹配
2. 实习岗位的发展潜力和学生的职业目标是否匹配
3. 公司提供的培训和发展机会是否符合学生的学习需求
4. 工作地点和工作时间是否符合学生的实际情况

如果相对而言匹配返回且仅返回YES，反之返回且仅返回NO。
'''

def whether_suitable(user_input, condensed_internship_info, zhipuai_API_KEY=zhipuai_API_KEY):
    if user_input == '':
        print('输入为空，请重新输入')
    else:
        client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": acquirement.format(stu_info=user_input, info=condensed_internship_info)}
            ],
            max_tokens=5
        )
    return response.choices[0].message.content
