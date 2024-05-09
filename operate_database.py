from database import database_operation

db_manager = database_operation.DatabaseManager()
db_manager.create_table('answers')
db_manager.insert(table_name='answers', key_answer='key1', whole_answer='whole answer 1')
db_manager.query('answers', "KEY_ANSWER = 'key1'")
db_manager.update('answers', 'new_key', 'updated answer', "KEY_ANSWER = 'key1'")
db_manager.delete('answers', "KEY_ANSWER = 'new_key'")
db_manager.close()