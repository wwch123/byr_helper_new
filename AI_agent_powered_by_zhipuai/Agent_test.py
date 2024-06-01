zhipuai_API_KEY='78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy'#hhz新API key 有效期到2024.6.10


import time
from zhipuai import ZhipuAI

user_input = input()
if user_input == '':
    print('输入为空，请重新输入')
else:
    client = ZhipuAI(api_key=zhipuai_API_KEY)  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            #{"role": "system", "content": background_info},
            {"role": "user", "content": user_input}
        ],
        max_tokens=500
    )


    print(response)

