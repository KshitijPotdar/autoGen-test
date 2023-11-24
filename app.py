import autogen
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

loaders = [ PyPDFLoader('./uniswap_v3.pdf') ]
docs = []
for l in loaders:
    docs.extend(l.load())
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(docs)

vectorstore = Chroma(
    collection_name="full_documents",
    
)
vectorstore.add_documents(docs)

qa = ConversationalRetrievalChain.from_llm(
   
    vectorstore.as_retriever(),
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)

result = qa(({"question": "What is uniswap?"}))
result = qa(({'answer'}))

def answer_uniswap_question(question):
  response = qa({"question": question})
  return response["answer"]


config_list = [
    {
        'api_type': '',
        'api_base': "http://localhost:1234/v1",
        'api_key': 'NULL'
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    
    "functions": [
        {
            "name": "answer_uniswap_question",
            "description": "Answer any Uniswap related questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask in relation to Uniswap protocol",
                    }
                },
                "required": ["question"],
            },
        }
    ],
}

assistant = autogen.AssistantAgent(
    name="Teacher",
    llm_config=llm_config,
    system_message="You are a Grade 8th Math teacher in New Zealand"
)



user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode= "NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content","").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved otherwise, reply CONTINUE""",
    function_map={"answer_uniswap_question": answer_uniswap_question}
)



task = """
            what are AMMs ?
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)