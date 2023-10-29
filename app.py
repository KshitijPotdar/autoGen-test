import autogen

config_list = [
    {
        'model': '',
        'api_key': ''
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="Senior developer in an EdTech company in New Zealand"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode= "TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content","").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved otherwise, reply CONTINUE"""
)

task = """
    Give me a summary of Oliver Twist
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)