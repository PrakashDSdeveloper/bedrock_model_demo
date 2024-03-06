import os
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import redshift_connector

def demo_chatbot():
    demo_llm = Bedrock(
        credentials_profile_name='default',
        region_name='us-east-1',
        model_id='meta.llama2-70b-chat-v1',
        model_kwargs={
            "temperature": 0.9,
            "top_p": 0.5,
            "max_gen_len": 512
        }
    )
    return demo_llm

def demo_memory():
    llm_data = demo_chatbot()
    memory = ConversationBufferMemory(llm=llm_data, max_token_limit=512)
    return memory

def demo_conversation(input_text, memory):
    conn = redshift_connector.connect(
        database='development',
        user='awsuser',
        password='Prakash-123456',
        host='my-redshift-cluster.cst1nhbptfv8.us-east-1.redshift.amazonaws.com',
        port=5439
    )
    cursor = conn.cursor()

    if input_text.lower() == "get all employees":
        query = "SELECT * FROM employement_data;"
        cursor.execute(query)
        rows = cursor.fetchall()
        response = "\n".join([str(row) for row in rows])
    elif input_text.lower() == "get employee count":
        query = "SELECT COUNT(*) FROM employement_data;"
        cursor.execute(query)
        rows = cursor.fetchall()
        response = "\n".join([str(row) for row in rows])
    elif input_text.lower().startswith("get employee"):
        employee_id = input_text.split()[-1]
        query = f"SELECT * FROM employement_data WHERE id = {employee_id};"
        cursor.execute(query)
        rows = cursor.fetchall()
        response = "\n".join([str(row) for row in rows])
    else:
        response = "Sorry, I don't understand that question."

    # if query:
    #     cursor.execute(query)
    #     rows = cursor.fetchall()
    #     response = "\n".join([str(row) for row in rows])
    # else:
    #     # response = "Sorry, I don't understand that question."
    #     pass

    cursor.close()
    conn.close()

    return response


# import os
# from langchain.llms.bedrock import Bedrock
# from langchain.chains import ConversationChain

# def demo_chatbot():
#     demo_llm = Bedrock(
#         credentials_profile_name='default',
#         region_name='us-east-1',
#         model_id='meta.llama2-70b-chat-v1',
#         model_kwargs={
#             "temperature": 0.9,
#             "top_p": 0.5,
#             "max_gen_len": 512
#         }
#     )
#     return demo_llm

# def demo_conversation(input_text):
#     llm = demo_chatbot()
#     llm_conversation = ConversationChain(llm=llm, verbose=True)
#     chat_reply = llm_conversation.predict(input=input_text)
#     return chat_reply
