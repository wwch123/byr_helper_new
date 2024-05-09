
from AI_agent_powered_by_zhipuai import Agent_01_classify_questions,Agent_02_emotional_companion,Agent_03_give_normal_answer
from AI_agent_powered_by_zhipuai import  Agent_04_memory,Agent_05_is_coherent

zhipuai_API_KEY='9d55fe81e5d814d15a178b6884fd4566.KeHWIwzewSoR0EQS'
if __name__ == '__main__':
    user_input=input()

    while user_input!='':
        round=1
        if round>1:
            coherence=Agent_05_is_coherent.is_coherent('用户输入：'+pre_input+'LLM回复：'+pre_answer+'用户输入：'+user_input)
            if coherence=='NO':classification=Agent_01_classify_questions.get_classification(user_input,zhipuai_API_KEY)
            else:classification=pre_classification
            if classification=='情感生活':
                answer=Agent_02_emotional_companion.get_emotional_support(user_input,zhipuai_API_KEY)
                print(answer)
            elif classification=='None':
                answer=Agent_03_give_normal_answer.get_normal_answer(user_input,zhipuai_API_KEY)
                print(answer)
            elif classification=='实习':
                print('6666666666666666666')
        else:
            classification = Agent_01_classify_questions.get_classification(user_input,zhipuai_API_KEY)
            if classification=='情感生活':
                answer=Agent_02_emotional_companion.get_emotional_support(user_input,zhipuai_API_KEY)
                print(answer)
            elif classification=='None':
                answer=Agent_03_give_normal_answer.get_normal_answer(user_input,zhipuai_API_KEY)
                print(answer)
            elif classification=='实习':
                print('6666666666666666666')
        pre_input=user_input
        pre_answer=answer
        pre_classification=classification
        print('PRE:'+str(pre_classification))
        print(str(classification))
        round+=1
        user_input=input()