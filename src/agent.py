import os

import matplotlib.pyplot as plt

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
        commander = AssistantAgent(
            name="Orchestrator",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            system_message="Help me run the code, and tell other agents it is in the <img result.jpg> file location.",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"last_n_messages": 3, "work_dir": self.working_dir, "use_docker": False},
            llm_config=self.llm_config,
        )

        evaluator = MultimodalConversableAgent(
            name="Evaluator",
            system_message="""Criticize the input figure. How to replot the figure so it will be better? Find bugs and issues for the figure.
            Pay attention to the color, format, and presentation. Keep in mind of the reader-friendliness.
            If you think the figures is good enough, then simply say NO_ISSUES""",
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
            + "ALWAYS save the figure in `result.jpg` file. Tell other agents it is in the <img result.jpg> file location."
        )

        # Data flow begins
        commander.initiate_chat(player, message=user_question)
        img = Image.open(os.path.join(self.working_dir, "result.jpg"))
        plt.imshow(img)
        plt.axis("off")  # Hide the axes
        plt.show()

        for i in range(self._n_iters):
            commander.send(
                message=f"Improve <img {os.path.join(self.working_dir, 'result.jpg')}>",
                recipient=evaluator,
                request_reply=True,
            )

            feedback = commander._oai_messages[evaluator][-1]["content"]
            if feedback.find("NO_ISSUES") >= 0:
                break
            commander.send(
                message="Here is the feedback to your figure. Please improve! Save the result to `result.jpg`\n"
                + feedback,
                recipient=player,
                request_reply=True,
            )
            img = Image.open(os.path.join(self.working_dir, "result.jpg"))
            plt.imshow(img)
            plt.axis("off")  # Hide the axes
            plt.show()

        return True, os.path.join(self.working_dir, "result.jpg")