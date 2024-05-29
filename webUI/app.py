from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Markup
import pymysql
import bcrypt
from datetime import datetime
import markdown

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 替换为你的实际密钥

zhipuai_API_KEY = '78d4d54ffce51ba65a99e12a87e2c1e2.NXKksWcbl2LBaYqy'

# 数据库配置
config = {
    'host': '110.41.49.124',
    'port': 3306,
    'user': 'root',
    'password': '@HWSJKmimashi111',
    'db': 'user_data',
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
        cursorclass=pymysql.cursors.DictCursor
    )

# 获取用户历史记录
def get_history(user_id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, question, answer, timestamp FROM history WHERE user_id = %s ORDER BY timestamp DESC"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

# 添加历史记录
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

# 用户注册或登录
def register_or_login(username, password):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_id, password_hash FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8')):
                    return ('login', result['user_id'])
                else:
                    return ('error', '密码错误')
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
                cursor.execute(sql, (username, hashed_password))
                connection.commit()
                return ('register', cursor.lastrowid)
    finally:
        connection.close()

# 创建表
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

create_tables()

def get_answer(user_input, api_key):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Markdown 转 HTML 方法
def md_to_html(md_content):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables', 'markdown.extensions.toc']
    html = markdown.markdown(md_content, extensions=exts)
    return Markup(html)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            return jsonify({"status": "error", "message": "请输入您的账号"})
        if not password:
            return jsonify({"status": "error", "message": "请输入您的密码"})
        action, user_info = register_or_login(username, password)
        if action == 'login':
            session['user_id'] = user_info
            return jsonify({"status": "success", "message": "登录成功"})
        elif action == 'register':
            session['user_id'] = user_info
            return jsonify({"status": "success", "message": "注册成功"})
        elif action == 'error':
            return jsonify({"status": "error", "message": user_info})

    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("请登录以查看主页。", "warning")
        return redirect(url_for('login'))

    user_history = get_history(session['user_id'])
    return render_template('home.html', history=user_history)

@app.route('/ask', methods=['POST'])
def ask():
    if 'user_id' not in session:
        return jsonify({"error": "请登录以保存您的问答记录。"})

    question = request.form.get('question')
    if question:
        answer_md = get_answer(question, zhipuai_API_KEY)
        answer_html = md_to_html(answer_md)
        add_history(session['user_id'], question, answer_md)
        return jsonify({"question": question, "answer": answer_html})

    return jsonify({"error": "未能获取问题。"})

@app.route('/history/<int:record_id>')
def get_history_record(record_id):
    if 'user_id' not in session:
        return jsonify({"error": "请登录以查看历史记录。"})

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT question, answer FROM history WHERE id = %s AND user_id = %s"
            cursor.execute(sql, (record_id, session['user_id']))
            result = cursor.fetchone()
            if result:
                result['answer'] = md_to_html(result['answer'])
                return jsonify(result)
            else:
                return jsonify({"error": "未找到历史记录。"})
    finally:
        connection.close()

@app.route('/wechat_login')
def wechat_login():
    # 这里处理微信登录逻辑，跳转到微信登录页面或生成二维码
    # 假设我们直接跳转到微信登录页面
    return redirect("https://open.weixin.qq.com/connect/qrconnect?appid=YOUR_APP_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect")

if __name__ == '__main__':
    app.run(debug=True)
