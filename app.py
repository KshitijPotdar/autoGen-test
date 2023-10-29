import autogen

config_list = [
    {
        'api_type': 'open_ai',
        'api_base': "http://localhost:1234/v1",
        'api_key': 'NULL'
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="Teacher",
    llm_config=llm_config,
    system_message="You are a Grade 8th Math teacher in New Zealand"
)

student = autogen.AssistantAgent(
    name="CuriousStudent",
    llm_config=llm_config,
    system_message="You are a curious student in an 8th grade math class in New Zealand. You ask questions about the answer given by the Teacher"
)

Fact_checker = autogen.AssistantAgent(
    name= "Fact Checker",
    llm_config=llm_config,
    system_message="You analyse the teacher's anwser to the user_proxy's question and reply if it has any mistakes"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode= "ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content","").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved otherwise, reply CONTINUE"""
)



task = """
            what is pythagoras theorem and solve a simple pythagoras problem and store it in a file.
"""



user_proxy.initiate_chat(
    assistant,

    message=task
)