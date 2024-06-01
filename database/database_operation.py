import pymysql

class DatabaseManager(object):
    def __init__(self, host = '110.41.49.124' ,user = "root" ,passwd="@HWSJKmimashi111",port= 3306,db="byr_helper" ,charset='utf8'):
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

    def create_postgraduate_info_table(self, table_name='postgraduate_info'):
        if not self.cursor:
            self.create_cursor()
        # 检查数据库中是否已存在该表
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = self.cursor.fetchone()
        if result:
            print(f"表 '{table_name}' 已经存在。")
        else:
            # 创建表
            sql = """
                        CREATE TABLE IF NOT EXISTS postgraduate_info (
                            serial_number INT PRIMARY KEY AUTO_INCREMENT,
                            key_info VARCHAR(255),
                            whole_info TEXT
                        )
                        """
            self.cursor.execute(sql)
            print(f"表 '{table_name}' 创建成功。")

    def create_internship_info_table(self, table_name='internship_info'):
        if not self.cursor:
            self.create_cursor()
        # 检查数据库中是否已存在该表
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = self.cursor.fetchone()
        if result:
            print(f"表 '{table_name}' 已经存在。")
        else:
            # 创建表
            sql = """
                        CREATE TABLE IF NOT EXISTS internship_info (
                            serial_number INT PRIMARY KEY AUTO_INCREMENT,
                            key_info VARCHAR(255),
                            whole_info TEXT
                        )
                        """
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

        # 获取当前表中最大的serial_number值
        sql_max_serial_number = f"SELECT MAX(serial_number) FROM {table_name}"
        self.cursor.execute(sql_max_serial_number)
        max_serial_number = self.cursor.fetchone()[0]

        # 确保serial_number是唯一的
        if max_serial_number is not None:
            serial_number = max_serial_number + 1
        else:
            serial_number = 1

        # 构建SQL语句并执行插入操作
        sql = "INSERT INTO {} (serial_number, key_info, whole_info) VALUES (%s, %s, %s)".format(table_name)
        self.cursor.execute(sql, (serial_number, key_answer, whole_answer))
        self.connection.commit()
        print(f"在表 '{table_name}' 中插入了一条记录。serial_number: {serial_number}")

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

    def get_form_content(self, table_name):
        """
        根据表单名称查询特定表单并打印表单内容
        :param table_name: 表单名称
        """
        if not self.cursor:
            self.create_cursor()

        # 检查数据库中是否已存在该表
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = self.cursor.fetchone()

        if result:
            # 查询表单内容
            sql = f"SELECT * FROM {table_name}"
            self.cursor.execute(sql)
            form_content = self.cursor.fetchall()

            print(f"表单 '{table_name}' 的内容如下：")
            for content in form_content:
                print(content)
        else:
            print(f"表单 '{table_name}' 不存在。")

    def delete_all_tables(self):
        if not self.cursor:
            self.create_cursor()

        # 获取所有表的列表
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        # 逐个删除表
        for table in tables:
            table_name = table[0]  # 表名在元组的第一个元素中
            print(f"正在删除表 '{table_name}'...")
            self.cursor.execute(f"DROP TABLE {table_name}")

        # 提交更改
        self.connection.commit()
        print("所有表都已删除。")
    def clear_table(self, table_name='postgraduate_info'):
        if not self.cursor:
            self.create_cursor()
        sql = f"DELETE FROM {table_name}"
        self.cursor.execute(sql)
        self.connection.commit()
        print(f"已清空表 '{table_name}' 中的所有记录。")

    def entry_exists(self, title, clarified_content):
        if not self.cursor:
            self.create_cursor()
        self.cursor.execute("SELECT COUNT(*) FROM postgraduate_info WHERE title = %s AND condensed_content = %s", (title, clarified_content))
        if self.cursor.fetchone()[0] > 0:
            return True
        else:
            return False

    def get_postgraduate_info_by_serial_number(self, serial_number):
        try:
            if not self.cursor:
                self.create_cursor()
            # 查询指定serial_number的记录
            sql = "SELECT key_info, whole_info FROM postgraduate_info WHERE serial_number = %s"
            self.cursor.execute(sql, (serial_number,))
            result = self.cursor.fetchone()
            if result:
                key_info, whole_info = result
                return key_info, whole_info
            else:
                print(f"没有找到serial_number为{serial_number}的记录。")
                return None, None
        except pymysql.MySQLError as e:
            print(f"数据库操作出错：{e}")
            return None, None
        except Exception as e:
            print(f"发生未知错误：{e}")
            return None, None
