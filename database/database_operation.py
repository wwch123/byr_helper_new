#数据库的基本信息，下面代码创建类的时候设有默认值
'''
db = pymysql.connect(host='117.78.9.167'
                     , user="root"
                     , passwd="Hhz200461"
                     , port=3306
                     , db="agent_data"  # 数据库名称
                     , charset='utf8mb4'  # 字符编码
                     )
                     '''

import pymysql

class DatabaseManager(object):
    def __init__(self, host='117.78.9.167', user="root", passwd="Hhz200461", port=3306, db="agent_data" , charset='utf8mb4'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
        self.charset = charset
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            port=self.port,
            db=self.db,
            charset=self.charset
        )
        print('数据库连接成功')
        return self.connection

    def create_cursor(self):
        if not self.connection:
            self.connect()
        self.cursor = self.connection.cursor()
        return self.cursor

    def create_table(self, table_name):
        if not self.cursor:
            self.create_cursor()
        # 检查数据库中是否已存在该表
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = self.cursor.fetchone()
        if result:
            print(f"表 '{table_name}' 已经存在。")
        else:
            # 创建表
            sql = f'''
              CREATE TABLE {table_name}
              (
              KEY_ANSWER varchar(255),
              WHOLE_ANSWER varchar(2047)
              )
              '''
            self.cursor.execute(sql)
            print(f"表 '{table_name}' 创建成功。")

    def show_tables(self):
        if not self.cursor:
            self.create_cursor()
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        for table in tables:
            print(table)

    def close(self):
        if self.cursor:
            self.cursor.close()
            print('游标已关闭')
        if self.connection:
            self.connection.close()
            print('数据库连接已关闭')

    def insert(self, table_name, key_answer, whole_answer):
        if not self.cursor:
            self.create_cursor()
        sql = "INSERT INTO {} (KEY_ANSWER, WHOLE_ANSWER) VALUES (%s, %s)".format(table_name)
        self.cursor.execute(sql, (key_answer, whole_answer))
        self.connection.commit()
        print(f"在表 '{table_name}' 中插入了一条记录。")

    def query(self, table_name, condition=None):
        if not self.cursor:
            self.create_cursor()
        sql = "SELECT KEY_ANSWER, WHOLE_ANSWER FROM {}".format(table_name)
        if condition:
            sql += " WHERE {}".format(condition)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(f"从表 '{table_name}' 中查询到了 {len(results)} 条记录。")
        return results

    def update(self, table_name, key_answer, whole_answer, condition):
        if not self.cursor:
            self.create_cursor()
        sql = "UPDATE {} SET KEY_ANSWER = %s, WHOLE_ANSWER = %s WHERE {}".format(table_name, condition)
        self.cursor.execute(sql, (key_answer, whole_answer))
        self.connection.commit()
        print(f"更新了表 '{table_name}' 中的记录。")

    def delete(self, table_name, condition):
        if not self.cursor:
            self.create_cursor()
        sql = "DELETE FROM {} WHERE {}".format(table_name, condition)
        self.cursor.execute(sql)
        self.connection.commit()
        print(f"从表 '{table_name}' 中删除了记录。")
# 使用示例
'''
db_manager = DatabaseManager('117.78.9.167', 'root', 'Hhz200461', 3306, 'agent_data')
db_manager.create_table('answers')
db_manager.show_tables()
db_manager.close()
'''
