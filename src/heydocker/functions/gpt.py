import logging
import os

import openai

from heydocker.functions import functions

logger = logging.getLogger(__name__)

openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_version = "2023-07-01-preview"
openai.api_type = "azure"


class GPTClient:
    def __init__(self, functions):
        self.header = {
            "role": "system",
            "content": "You are a helpful assistant on a chat app. You can help user to monitor, remote, and control their server. Don't make assumptions about what values to use with functions. Ask for clarification if a user request is ambiguous. Always answer with human-readable text.",
        }
        self.functions = functions
        self.history = []

    @property
    def messages(self):
        return [self.header] + self.history[-4:]

    def add_message(self, message):
        self.history.append(message)

    def handle_command(self, command):
        self.add_message(
            {
                "role": "user",
                "content": command,
            }
        )

        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo-0613",
            messages=self.messages,
            functions=self.functions,
            function_call="auto",
        )

        response_message = response["choices"][0]["message"]

        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = response_message["function_call"]["arguments"]

            command = f"functions.{function_name}(**{function_args})"
            try:
                logger.info(f"Execute Function: {command}")
                function_response = eval(command)
            except Exception as e:
                function_response = f"ERROR {e}"

            logger.info(f"Function Response: {function_response}")

            # Add the assistant response and function response to the messages
            self.add_message(
                {
                    "role": response_message["role"],
                    "function_call": {
                        "name": function_name,
                        "arguments": response_message["function_call"]["arguments"],
                    },
                    "content": None,
                }
            )

            self.add_message(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )

            # Call the API again to get the final response from the model
            second_response = openai.ChatCompletion.create(
                messages=self.messages,
                deployment_id="gpt-35-turbo-0613"
            )

            return second_response["choices"][0]["message"]["content"]
        
        else:
            return response_message["content"]


# def gpt_function_calling(messages, functions):
#     # messages = [
#     #     {
#     #         "role": "user",
#     #         "content": message,
#     #     }
#     # ]
#     response = openai.ChatCompletion.create(
#         engine="gpt-35-turbo-0613",
#         messages=messages,
#         functions=functions,
#         function_call="auto",
#     )

#     return response


# def gpt_chat(messages, command, data):
#     response = openai.ChatCompletion.create(
#         engine="gpt-35-turbo-0613",
#         # messages=[
#         #     {"role": "system", "content": "You are a helpful assistant on a chat app. The user wants to use you to monitor, remote, and control their server. Please reformat all the data into a human-readable format and make it suitable for the user's question."},
#         #     {
#         #         "role": "user",
#         #         "content": question,
#         #     },
#         #     {"role": "system", "content": f"The command '{command}' has been executed, and the output is: '{data}'. Please help me combine this result with the user's question and send it back to the user."},
#         # ],
#         messages=messages,
#     )

#     return response
