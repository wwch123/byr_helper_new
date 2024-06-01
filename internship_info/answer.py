from AI_agent_powered_by_zhipuai import Agent_judge_whether_you_need_more
from internship_info import Agent_whether_suitable,Agent_whether_suitable_double_check,Agent_analysis
from database import database_operation
from colorama import init, Fore
import sys

zhipuai_API_KEY = 'a1c585c7b8106e12b92ceae99026a2cd.frA1fHlR0O4lyba4'
init()
'''
instruction:
1. The only func you need is main_func
2. The way to use it i pointed next to the def as comment
'''
def get_internship_info_from_database(db, serial_number):
    try:
        cursor = db.cursor
        sql = 'SELECT key_info, whole_info FROM internship_info WHERE serial_number = %s'
        cursor.execute(sql, (serial_number,))
        result = cursor.fetchone()
        if result:
            print('############key_info###############')
            print(result[0])
            print('############whole_info#############')
            print(result[1])
            print('###################################')
            return result
        else:
            print(f"No information found for serial number {serial_number}")
            return None
    except Exception as e:
        print(f"Error retrieving postgraduate info: {e}")
        return None

def get_database_object():
    try:
        db = database_operation.DatabaseManager()
        db.connect()
        db.create_cursor()
        return db
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def whether_suitable(user_input, info):
    try:
        outcome = Agent_whether_suitable.whether_suitable(user_input,info[1])
        return outcome
    except Exception as e:
        print(f"Error calling suitability agent: {e}")
        return "NO"

def whether_suitable_double_check(user_input, info):
    try:
        outcome = Agent_whether_suitable_double_check.whether_suitable(user_input,info[1])
        return outcome
    except Exception as e:
        print(f"Error calling suitability agent: {e}")
        return "NO"

def get_suggestions(user_input,info):
    try:
        suggestions=Agent_analysis.get_suggestions(user_input,info[1])
        return suggestions
    except Exception as e:
        print(f"Error calling suitability agent: {e}")
        return None

#input: nothing (when you run the func, it will ask you to give the requirement of your further study
#workflow: give the requirement->return the suggestions and the postgraguda->ask you whether need more info->...
#output:plz design it by yourself
def main_func():
    db = get_database_object()

    serial_number = 0
    flag = 1
    print('请输入你的技能以及期待的实习岗位')
    user_input = input()

    while flag == 1:
        answers = []
        for i in range(5):
            serial_number += 1
            info = get_internship_info_from_database(db, serial_number)
            if info:
                outcome_one = whether_suitable(user_input, info)
                outcome_two = whether_suitable_double_check(user_input,info)
                print(outcome_one+'   '+outcome_two)
                if 'YES' in outcome_one and 'YES' in outcome_two:
                    suggestions=get_suggestions(user_input,info)
                    answers.append(info[1]+'建议如下：\n'+suggestions)

        print('已为您找到以下匹配内容：')
        print('***************************')
        print(answers)
        print('***************************')

        if len(answers) == 0:

            print('目前暂无匹配您需求的信息')
        else:
            for answer in answers:
                print(Fore.RED + answer)
        print(Fore.RESET + '请问您是否需要更多信息？')

        try:
            a = Agent_judge_whether_you_need_more.whether_need_more_info('请问您是否需要更多信息？', zhipuai_API_KEY)
            if 'YES' in a:
                pass
            else:
                flag = 0
        except Exception as e:
            print(f"Error calling need more info agent: {e}")
            flag = 0

    try:
        db.cursor.close()
        db.connection.close()
    except Exception as e:
        print(f"Error closing database resources: {e}")

main_func()

