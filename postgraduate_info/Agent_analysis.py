from zhipuai import ZhipuAI
import re

zhipuai_API_KEY='78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy'#hhz新API key 有效期到2024.6.10

acquirement='''
学生保研需求：{stu_info} ，
老师保研招生信息：{info}，
你是一个高级保研规划师，拥有丰富的行业经验以及保研经历，懂得学生的需求和保研中的人情世故
你需要帮我根据学生的保研需求和老师的保研招生信息帮我书写保研匹配度分析以及保研针对性建议
保研匹配度分析是指根据老师的招生信息和学生的需求分析两者匹配度
保研针对性建议是指根据老师的招生信息针对性的给学生一些保研的建议提升学生被录取的概率

要求格式如下：
"保研匹配度分析\n专业匹配度：(.*?)\n学位匹配度：(.*?)\n\n保研针对性建议\n申请材料建议：(.*?)\n套磁信书写建议：(.*?)\n其他建议：(.*?)\n"
'''

#extract_content()暂时没用
def extract_content(text):
    pattern = r'(保研匹配度分析\n专业匹配度：.*?\n学位匹配度：.*?\n\n保研针对性建议\n申请材料建议：.*?\n套磁信书写建议：.*?\n其他建议：.*?\n)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def get_suggestions(user_input,condensed_postgraduate_info,zhipuai_API_KEY=zhipuai_API_KEY):
    if user_input=='':
        print('输入为空，请重新输入')
    else:
        client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": acquirement.format(stu_info=user_input,info=condensed_postgraduate_info)}
            ],
            max_tokens=400
        )
    return response.choices[0].message.content


