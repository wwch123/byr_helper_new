from AI_agent_powered_by_zhipuai import Agent_judge_whether_you_need_more
from postgraduate_info import Agent_whether_suitable, Agent_whether_suitable_double_check, Agent_analysis
from database import database_operation
from colorama import init, Fore
import sys

zhipuai_API_KEY = 'a1c585c7b8106e12b92ceae99026a2cd.frA1fHlR0O4lyba4'
init()


def get_postgraduate_info_from_database(db, serial_number):
    try:
        cursor = db.cursor
        sql = 'SELECT key_info, whole_info FROM postgraduate_info WHERE serial_number = %s'
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
        print("Database connection and cursor creation successful.")
        return db
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def whether_suitable(user_input, info):
    try:
        outcome = Agent_whether_suitable.whether_suitable(user_input, info[0])
        print(f"Suitability check 1: {outcome}")
        return outcome
    except Exception as e:
        print(f"Error calling suitability agent: {e}")
        return "NO"


def whether_suitable_double_check(user_input, info):
    try:
        outcome = Agent_whether_suitable_double_check.whether_suitable(user_input, info[0])
        print(f"Suitability check 2: {outcome}")
        return outcome
    except Exception as e:
        print(f"Error calling suitability agent: {e}")
        return "NO"


def get_suggestions(user_input, info):
    try:
        suggestions = Agent_analysis.get_suggestions(user_input, info)
        print(f"Suggestions: {suggestions}")
        return suggestions
    except Exception as e:
        print(f"Error calling analysis agent: {e}")
        return None


def main_func(user_input, serial_number):
    db = get_database_object()
    results = []
    serial_number = serial_number
    flag = 1
    flag_1 = 0  # 检查是否检索完所有数据库
    print('Processing postgraduate application requirements...')
    answers = []
    try:
        while flag == 1 and flag_1 == 0:
            # answers = []
            while len(answers) < 2:
                serial_number += 1
                info = get_postgraduate_info_from_database(db, serial_number)
                if info:
                    outcome_one = whether_suitable(user_input, info)
                    outcome_two = whether_suitable_double_check(user_input, info)
                    print(outcome_one + '   ' + outcome_two)
                    if 'YES' in outcome_one and 'YES' in outcome_two:
                        suggestions = get_suggestions(user_input, info[1])
                        answers.append(info[1] + '\n\n——————————————__建议__——————————————\n' + suggestions)

            print('已为您找到以下匹配内容：')
            results.append('已为您找到以下匹配内容：')
            results.extend(answers)
            print('***************************')
            print(results)
            print('***************************')

            if len(answers) < 1:
                print('已全部检索完毕，无更多信息可查')
                results.append('已全部检索完毕，无更多信息可查')
                flag_1 = 1
            flag = 0  # 结束循环
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        try:
            db.cursor.close()
            db.connection.close()
            print("Database connection closed.")
        except Exception as e:
            print(f"Error closing database resources: {e}")

    print(f"Final results: {results}")

    return results, len(answers)

# Test the function
# a = main_func("我想保研到通信工程")
# print("Test finished, final output:")
# print(a)
