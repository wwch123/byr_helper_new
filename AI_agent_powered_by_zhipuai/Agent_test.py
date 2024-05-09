zhipuai_API_KEY="9d55fe81e5d814d15a178b6884fd4566.KeHWIwzewSoR0EQS"

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
        max_tokens=300
    )

for i in range(10):
    print(response)
    time.sleep(0.1)

