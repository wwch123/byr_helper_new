from zhipuai import ZhipuAI
import re

zhipuai_API_KEY='78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy' # 替换为你的API key，有效期到2024.6.10

acquirement='''
学生实习需求：{stu_info}，
公司实习岗位信息：{info}，
你是一个高级实习规划师，拥有丰富的行业经验以及实习经历，懂得学生的需求和实习中的人情世故
你需要帮我根据学生的实习需求和公司的实习岗位信息帮我书写实习匹配度分析以及实习针对性建议
实习匹配度分析是指根据公司的岗位信息和学生的需求分析两者匹配度
实习针对性建议是指根据公司的岗位信息针对性的给学生一些实习的建议提升学生被录取的概率

要求格式如下：
"实习匹配度分析\n岗位匹配度：(.*?)\n技能匹配度：(.*?)\n\n实习针对性建议\n申请材料建议：(.*?)\n求职信书写建议：(.*?)\n其他建议：(.*?)\n"
'''

def extract_content(text):
    pattern = r'(实习匹配度分析\n岗位匹配度：.*?\n技能匹配度：.*?\n\n实习针对性建议\n申请材料建议：.*?\n求职信书写建议：.*?\n其他建议：.*?\n)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def get_suggestions(user_input, condensed_internship_info, zhipuai_API_KEY=zhipuai_API_KEY):
    if user_input == '':
        print('输入为空，请重新输入')
    else:
        client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": acquirement.format(stu_info=user_input, info=condensed_internship_info)}
            ],
            max_tokens=400
        )
    return response.choices[0].message.content
