import streamlit as st
import pymysql
import bcrypt
from datetime import datetime
from zhipuai import ZhipuAI
zhipuai_API_KEY='78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy'
# 数据库配置
config = {
    'host': '110.41.49.124',  # 更新为你的数据库服务器地址
    'port': 3306,             # 更新为你的数据库端口，默认MySQL端口是3306
    'user': 'root',           # 更新为你的数据库用户名
    'password': '@HWSJKmimashi111', # 更新为你的数据库密码
    'db': 'user_data',       # 数据库名
    'charset': 'utf8mb4'
}

# 连接到数据库
def connect_db():
    return pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        db=config['db'],
        charset=config['charset'],
        cursorclass=pymysql.cursors.DictCursor  # 使用 DictCursor
    )

# 获取用户历史记录的函数
def get_history(user_id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, question, answer, timestamp FROM history WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

# 添加历史记录的函数
def add_history(user_id, question, answer):
    connection = connect_db()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO history (user_id, question, answer, timestamp) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, question, answer, timestamp))
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()

# 删除历史记录的函数
def delete_history(record_id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM history WHERE id = %s"
            cursor.execute(sql, (record_id,))
            connection.commit()
            return cursor.rowcount
    finally:
        connection.close()

# 用户注册或登录的函数
def register_or_login(username, password):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_id, password_hash FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                # 用户存在，检查密码
                if bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8')):
                    return ('login', result['user_id'])  # 返回登录成功和用户ID
                else:
                    return ('error', 'Incorrect password')
            else:
                # 用户不存在，创建新用户
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
                cursor.execute(sql, (username, hashed_password))
                connection.commit()
                return ('register', cursor.lastrowid)  # 返回注册成功和新用户ID
    finally:
        connection.close()


# 在数据库中创建必要的表
def create_tables():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash CHAR(60) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            create_history_table = """
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_users_table)
            cursor.execute(create_history_table)
            connection.commit()
    finally:
        connection.close()

def get_answer(user_input, api_key):
    # 创建 ZhipuAI 客户端
    client = ZhipuAI(api_key=api_key)

    # 发送请求并获取响应
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    # 处理并返回响应中的最后一个回答
    return response.choices[0].message.content


# Streamlit UI
def main():
    create_tables()
    st.markdown("""
            <style>
                .main-title {
                    
                    font-size: 3em;
                    font-weight: bold;
                    text-align: center;
                    color: #070707;
                }
                .maintitle-label {
                    margin-top: -50px;
                }
                .sub-title {
                    font-family: 'STXingkai',
                    font-size: 1em;
                    font-weight: normal;
                    margin-bottom: 0px;
                    color: #898B8D;
                }
                .stButton>button {
                    font-size: 1em;
                    padding: 10px 20px;
                    background-color: #070707;
                    border: none;
                    color: white;
                    border-radius: 5px;
                }
                .stButton>button:hover {
                    background-color: #45a049;
                }
                .sidebar .sidebar-content {
                    font-size: 1.2em;
                }
                /* 调整selectbox和标题之间的间距 */
                .selectbox-label {
                    margin-bottom: -40px;
                }
            </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='main-title maintitle-label'>💬 邮邮助手</div>", unsafe_allow_html=True)

    # 在selectbox上方添加自定义样式的标题
    st.sidebar.markdown("<div class='sub-title selectbox-label'>菜单</div>", unsafe_allow_html=True)
    menu = ['邮邮问答助手', '登录/注册', '查看历史记录']
    choice = st.sidebar.selectbox("",menu)

    if choice == '邮邮问答助手':
        st.markdown("<div class='sub-title'>欢迎来到问答助手——你的AI辅导员</div>", unsafe_allow_html=True)
        question = st.chat_input("输入您的问题并按回车发送")
        if question:
            answer = get_answer(question, zhipuai_API_KEY)
            st.markdown(f"**问**：{question}")
            st.markdown(f"**答**：{answer}")
            if 'user_id' in st.session_state:
                add_history(st.session_state['user_id'], question, answer)
            else:
                st.warning("您当前尚未登录，该问答记录不会被保存到历史记录中~")

    elif choice == '登录/注册':
        st.markdown("<div class='sub-title'>登录或注册</div>", unsafe_allow_html=True)
        username = st.sidebar.text_input("用户名")
        password = st.sidebar.text_input("密码", type='password')
        if st.sidebar.button("登录 / 注册"):
            action, user_info = register_or_login(username, password)
            if action == 'login':
                st.success(f"成功登录，用户名为 {username}。用户ID: {user_info}")
                st.session_state['user_id'] = user_info
            elif action == 'register':
                st.success(f"注册成功，用户名为 {username}。新用户ID: {user_info}")
                st.session_state['user_id'] = user_info
            elif action == 'error':
                st.error(user_info)

    elif choice == '查看历史记录':
        if 'user_id' in st.session_state:
            st.markdown("<div class='sub-title'>历史记录</div>", unsafe_allow_html=True)
            history = get_history(st.session_state['user_id'])
            if history:
                for record in history:
                    with st.expander(f"问题：{record['question']}"):
                        st.markdown(f"**答案**：{record['answer']}")
                        st.markdown(f"**时间**：{record['timestamp']}")
            else:
                st.write("未找到历史记录。")
        else:
            st.warning("请登录以查看历史记录。")


if __name__ == "__main__":
    main()
