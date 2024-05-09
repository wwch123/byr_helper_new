from selenium import webdriver
from selenium.webdriver.common.by import By  #选择器
from selenium.webdriver.common.keys import Keys   #按键
from selenium.webdriver.support.wait import WebDriverWait  #等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕
import time
from selenium.common.exceptions import NoSuchElementException
from docx import Document
class BeiYouSpider(object):
    def __init__(self):
        self.start_url = 'https://bbs.byr.cn/index'
        self.options = webdriver.ChromeOptions()  # 配置文件对象
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 无头模式
        self.broswer = webdriver.Chrome(options=self.options)  # 关闭文件对象
        self.broswer.implicitly_wait(10)

    def disembark(self):#用来进行登陆操作
        self.broswer.get(url=self.start_url)
        username = self.broswer.find_element(By.ID,'id')
        username.send_keys('wwch1123')
        password = self.broswer.find_element(By.ID,'pwd')
        password.send_keys('wwch20040728')
        dise_button = self.broswer.find_element(By.ID,'b_login')
        dise_button.click()

    def click_target_url(self,target_XPATH):#点击进入目标网页
        self.broswer.find_element(By.XPATH,target_XPATH).click()

    def get_content(self, target_XPATH):
        # 尝试获取目标内容
        try:
            target_content = self.broswer.find_element(By.XPATH, target_XPATH).text
            return target_content
        except NoSuchElementException:
            # 如果XPATH不正确，打印错误信息并返回None
            print(f"XPATH不正确：{target_XPATH}")
            return None




def write_content_to_docx(content, docx_path):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(docx_path)




'''docx_path=r"F:\桌面\byr_spider_database.docx"
beiyou = BeiYouSpider()
beiyou.disembark()
beiyou.click_target_url('//*[@id="xlist"]/ul/li[1]/ul/li[3]/span/a')
beiyou.click_target_url('/html/body/section/section/div[2]/table/tbody/tr[1]/td[1]/a')

beiyou.click_target_url('/html/body/section/section/div[3]/table/tbody/tr[8]/td[2]/a')
content=beiyou.get_content('/html/body/section/section/div[3]/div/table/tbody/tr[2]/td[2]/div')
write_content_to_docx(content,docx_path)'''

