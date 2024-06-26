from AI_agent_powered_by_zhipuai import Agent_01_classify_questions, Agent_02_emotional_companion, Agent_03_give_normal_answer
from AI_agent_powered_by_zhipuai import Agent_04_memory, Agent_05_is_coherent

zhipuai_API_KEY = '9d55fe81e5d814d15a178b6884fd4566.KeHWIwzewSoR0EQS'
if __name__ == '__main__':
    user_input = input()
    pre_answer = ''  # 初始定义一个默认的 answer
    round = 1
    pre_classification = None  # 初始定义 pre_classification

    while user_input != '':
        if round > 1:
            coherence = Agent_05_is_coherent.is_coherent('用户输入：' + pre_input + 'LLM回复：' + pre_answer + '用户输入：' + user_input,zhipuai_API_KEY)
            if coherence == 'NO':
                classification = Agent_01_classify_questions.get_classification(user_input, zhipuai_API_KEY)
            else:
                classification = pre_classification
        else:
            classification = Agent_01_classify_questions.get_classification(user_input, zhipuai_API_KEY)

        if classification == '情感生活':
            answer = Agent_02_emotional_companion.get_emotional_support(user_input, zhipuai_API_KEY)
            print(answer)
        elif classification == 'None':
            answer = Agent_03_give_normal_answer.get_normal_answer(user_input, zhipuai_API_KEY)
            print(answer)
        elif classification == '实习':
            answer = '6666666666666666666'
            print(answer)
        else:
            answer = '无法识别的输入类型'
            print(answer)

        pre_input = user_input
        pre_answer = answer
        pre_classification = classification
        print('PRE:' + str(pre_classification))
        print(str(classification))
        round += 1
        user_input = input()
