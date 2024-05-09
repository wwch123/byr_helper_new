import time

from spider import spider_selenium
from AI_agent_powered_by_zhipuai import Agent_condense_the_content

zhipuai_API_KEY='9d55fe81e5d814d15a178b6884fd4566.KeHWIwzewSoR0EQS'
docx_path=r"F:\桌面\byr_spider_database.docx"

docx_path=r"F:\桌面\byr_spider_database.docx"
beiyou = spider_selenium.BeiYouSpider()
beiyou.disembark()
print('已登录')
print('\n',end='')
'''
beiyou.click_target_url('/html/body/aside/nav/ul/li[1]/ul/li[4]/span/a') #点击‘信息社会’

beiyou.click_target_url('/html/body/section/section/div[2]/table/tbody/tr[23]/td[1]/a')#点击‘兼职实习信息'

beiyou.click_target_url('/html/body/section/section/div[3]/table/tbody/tr[6]/td[2]/a')
'''
#/html/body/section/section/div[3]/table/tbody/tr[7]/td[2]/a

#/html/body/section/section/div[3]/table/tbody/tr[30]/td[2]/a
for i in range(1,3,1):
    if i==1:
        for j in range(6,31,1):
            beiyou.click_target_url('/html/body/section/section/div[3]/table/tbody/tr[{num}]/td[2]/a'.format(num=str(j)))
            print('已找到目标内容')
            print('\n', end='')

            # 假设 beiyou.get_content() 在成功获取内容时返回内容字符串，在失败时返回None
            content = beiyou.get_content('/html/body/section/section/div[3]/div/table/tbody/tr[2]/td[2]/div')

            # 判断是否成功获取了content
            if content:
                print('以下为目标爬取内容：')
                print(content)
                print('\n', end='')

                # 假设 Agent_condense_the_content.get_condensed_content() 需要一个非空的content
                condensed_content = Agent_condense_the_content.get_condensed_content(content, zhipuai_API_KEY)
                print('以下为浓缩之后的内容：')
                print(condensed_content)
                print('\n', end='')
            else:
                print('未获取到内容，跳过处理。\n', end='')

    else:
        for j in range(1,31,1):
            beiyou.click_target_url(
                '/html/body/section/section/div[3]/table/tbody/tr[{num}]/td[2]/a'.format(num=str(j)))
            print('已找到目标内容')
            print('\n', end='')

            # 假设 beiyou.get_content() 在成功获取内容时返回内容字符串，在失败时返回None
            content = beiyou.get_content('/html/body/section/section/div[3]/div/table/tbody/tr[2]/td[2]/div')

            # 判断是否成功获取了content
            if content:
                print('以下为目标爬取内容：')
                print(content)
                print('\n', end='')

                # 假设 Agent_condense_the_content.get_condensed_content() 需要一个非空的content
                condensed_content = Agent_condense_the_content.get_condensed_content(content, zhipuai_API_KEY)
                print('以下为浓缩之后的内容：')
                print(condensed_content)
                print('\n', end='')
            else:
                print('未获取到内容，跳过处理。\n', end='')


