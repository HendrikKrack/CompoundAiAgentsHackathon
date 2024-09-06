import autogen

from agent import PlaywrightAgent

config_list = [
    {
        "api_type": "bedrock",
        "model": "anthropic.claude-3-sonnet-20240229-v1:0",
        "aws_region": "us-west-2",
        # "aws_profile_name": "",
        "temperature": 0.0,
    }
]

def main():
    llm_config = {
        "config_list": config_list,
    }

    playwright = PlaywrightAgent(name="Playwright Agent~", working_dir=".", llm_config=llm_config)

    user_proxy = autogen.UserProxyAgent(
        name="User", human_input_mode="NEVER", max_consecutive_auto_reply=0, code_execution_config={"use_docker": False}
    )

    user_proxy.initiate_chat(
        playwright,
        message="""
    Plot a figure by using the data from:
    https://raw.githubusercontent.com/vega/vega/main/docs/data/seattle-weather.csv

    I want to show both temperature high and low.
    """,
    )
    
    # image_agent = MultimodalConversableAgent(
    #     name="test-recording-evaluator",
    #     max_consecutive_auto_reply=10,
    #     llm_config={
    #         "config_list": config_list,
    #         "temperature": 0.1,
    #         "max_tokens": 300,
    #     },
    # )

    # user_proxy = autogen.UserProxyAgent(
    #     name="User_proxy",
    #     system_message="A human admin.",
    #     human_input_mode="NEVER",  # Try between ALWAYS or NEVER
    #     max_consecutive_auto_reply=0,
    #     code_execution_config={
    #         "use_docker": False
    #     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    # )

    # user_proxy.initiate_chat(
    # image_agent,
    # message="""What's the breed of this dog?
    # <img https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0>.""",
    # )

# def main():
#     # Load LLM inference endpoints from an env variable or a file
#     # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
#     # and OAI_CONFIG_LIST_sample.
#     # For example, if you have created a OAI_CONFIG_LIST file in the current working directory, that file will be used.
#     # config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

#     # Create the agent that uses the LLM.
#     assistant = ConversableAgent("agent", llm_config={"config_list": config_list})

#     # Create the agent that represents the user in the conversation.
#     user_proxy = UserProxyAgent("user", code_execution_config=False)

#     # Let the assistant start the conversation.  It will end when the user types exit.
#     assistant.initiate_chat(user_proxy, message="How can I help you today?")


if __name__ == "__main__":
    main()