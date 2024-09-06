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

# Patch .\.venv\Lib\site-packages\autogen\agentchat\contrib\multimodal_conversable_agent.py
# if isinstance(message, str):
#     out =  {"content": gpt4v_formatter(message, img_format="pil")}
#     # Filter elements where 'type' is 'text' and 'text' is empty
#     out["content"] = [item for item in out["content"] if not (item.get("type") == "text" and item.get("text") == "")]
#     return out
def main():
    llm_config = {
        "config_list": config_list,
    }

    playwright = PlaywrightAgent(name="Playwright Agent~", working_dir="./test-results", llm_config=llm_config)

    user_proxy = autogen.UserProxyAgent(
        name="User", human_input_mode="NEVER", max_consecutive_auto_reply=0, code_execution_config={"use_docker": False}
    )

    user_proxy.initiate_chat(
        playwright,
        message="""
Test 1: Should load homepage successfully
    Description: This test verifies that the homepage of the website loads correctly. When the test runs, the browser opens the homepage, displaying the title "Home Page" and the welcome message "Welcome to the homepage." The test checks if these elements are present and visible to the user. The test passes without any issues, confirming that the homepage loads as expected.

Test 2: Should log in successfully
    Description: This test simulates a user attempting to log in to the website. It inputs valid login credentials and submits the form. Upon successful login, the test checks if the user is redirected to the appropriate page or if a success message is displayed. The test passes, confirming that the login functionality works as expected with valid credentials.

Test 3: Should fail to load a non-existent page
    Description: This test attempts to access a page on the website that does not exist. The browser navigates to the invalid URL, and the test expects the page to return a "404 - Page Not Found" error. The test fails because it either timed out or encountered an unexpected issue during navigation. A screenshot and video were captured to help diagnose the issue.

These tests validate basic user interactions like loading pages and logging in, with the last one confirming how the system handles invalid page requests.
    """,
    )

if __name__ == "__main__":
    main()