import autogen

from agent import PlaywrightAgent

from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

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

#     playwright = PlaywrightAgent(name="Playwright Agent~", working_dir=".", llm_config=llm_config)

#     user_proxy = autogen.UserProxyAgent(
#         name="User", human_input_mode="NEVER", max_consecutive_auto_reply=0, code_execution_config={"use_docker": False}
#     )

#     user_proxy.initiate_chat(
#         playwright,
#         message="""
# Test 1: Should load homepage successfully
#     Description: This test verifies that the homepage of the website loads correctly. When the test runs, the browser opens the homepage, displaying the title "Home Page" and the welcome message "Welcome to the homepage." The test checks if these elements are present and visible to the user. The test passes without any issues, confirming that the homepage loads as expected.

# Test 2: Should log in successfully
#     Description: This test simulates a user attempting to log in to the website. It inputs valid login credentials and submits the form. Upon successful login, the test checks if the user is redirected to the appropriate page or if a success message is displayed. The test passes, confirming that the login functionality works as expected with valid credentials.

# Test 3: Should fail to load a non-existent page
#     Description: This test attempts to access a page on the website that does not exist. The browser navigates to the invalid URL, and the test expects the page to return a "404 - Page Not Found" error. The test fails because it either timed out or encountered an unexpected issue during navigation. A screenshot and video were captured to help diagnose the issue.

# These tests validate basic user interactions like loading pages and logging in, with the last one confirming how the system handles invalid page requests.
#     """,
#     )
    
    image_agent = MultimodalConversableAgent(
        name="test-recording-evaluator",
        max_consecutive_auto_reply=10,
        llm_config={
            "config_list": config_list,
            "temperature": 0.1,
            "max_tokens": 300,
        },
    )

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        human_input_mode="NEVER",  # Try between ALWAYS or NEVER
        max_consecutive_auto_reply=0,
        code_execution_config={
            "use_docker": False
        },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    )

    user_proxy.initiate_chat(
    image_agent,
    message="""What's the breed of this dog?
    <img https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0>.""",
    )

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