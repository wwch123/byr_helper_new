'''
# 目标登录页面URL
login_url = 'http://my.bupt.edu.cn/xs_index.jsp?urltype=tree.TreeTempUrl&wbtreeid=1541'

# 用户的登录信息，实际使用时请替换为正确的用户名和密码
login_data = {
    'id': 'wwch1123',
    'password': 'wwch20040728'
}

# 设置请求头，模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}
'''

import requests


session = requests.Session()
url = "https://www.bv2008.cn/app/user/login.php?m=login"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

data = {
    'seid': '7927a0bedf302b069d57851ee88e98e7',
    'uname': 'wwch234',
    'upass': 'Wwch20040728',
    'referer': 'https://www.bv2008.cn/app/user/home.php',
    'uyzm':''
}

# session对象登录，记录登录的状态
html = session.post(url=url, headers=headers, data=data)
next_url='https://bbs.byr.cn/#!article/ACM_ICPC/100716'
print(html.text)
'''# session对象的登录的状态去请求
url_main = 'https://bbs.byr.cn/#!article/ACM_ICPC/100716'
html = session.get(url_main, headers=headers)
#html.encoding = 'utf-8'
print(html.text)'''


