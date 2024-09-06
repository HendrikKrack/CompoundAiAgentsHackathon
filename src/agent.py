import json
import os

from PIL import Image

from autogen import Agent, AssistantAgent, ConversableAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent


class PlaywrightAgent(ConversableAgent):
    def __init__(self, working_dir=".", n_iters=2, **kwargs):
        super().__init__(**kwargs)
        self.register_reply([Agent, None], reply_func=PlaywrightAgent._reply_user, position=0)
        self.working_dir = working_dir
        self._n_iters = n_iters

    def _reply_user(self, messages=None, sender=None, config=None):
        if all((messages is None, sender is None)):
            error_msg = f"Either {messages=} or {sender=} must be provided."
            print(error_msg)
            raise AssertionError(error_msg)
        if messages is None:
            messages = self._oai_messages[sender]

        user_question = messages[-1]["content"]

        ### Define the agents
        orchestrator = AssistantAgent(
            name="Orchestrator",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            system_message="Help me run the test by coordinating with other agents.",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"last_n_messages": 3, "work_dir": self.working_dir, "use_docker": False},
            llm_config=self.llm_config,
        )

        evaluator = MultimodalConversableAgent(
            name="Evaluator",
            system_message="""You are given Playwright test result along with screenshots of the test execution
            in the browser. You are also given a list of test test expectations. You are responsible for assessing
            whether all test expectations are met given the test results and screenshots of the test execution.
            For each test expectation, say whether it was successfully passed or failed. If failed, provide a detailed
            explanation of why it failed given the test results and screenshots of the test execution. You MUST output
            your response in JSON format.
            """,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            #     use_docker=False,
        )

        player = AssistantAgent(
            name="Player",
            llm_config=self.llm_config,
        )

        player.update_system_message(
            player.system_message
            + "ALWAYS save the test result and screenshots in the result directory. Tell other agents it is in the 'result' directory."
        )

        # # Data flow begins
        # orchestrator.initiate_chat(player, message=user_question)
        # Open results json file
        with open(os.path.join(self.working_dir, "result.json"), "r") as f:
            result = json.load(f)
        # Open all screenshots
        screenshots = []
        screenshot_paths = []
        for filename in os.listdir(self.working_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'result.jpg':
                img_path = os.path.join(self.working_dir, filename)
                img = Image.open(img_path)
                screenshots.append(img)
                screenshot_paths.append(img_path)

        msg = f"""
        Here is the test result:
        {result}
        """
        for i, _ in enumerate(screenshots):
            msg += f"""<img {screenshot_paths[i]}>"""

        orchestrator.send(
            message=msg,
            recipient=evaluator,
            request_reply=True,
        )

        feedback = orchestrator._oai_messages[evaluator][-1]["content"]

        return True, feedback