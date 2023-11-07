import inspect
import logging
import os

import openai
from docstring_parser import parse

from heydocker.config import get_openai_api_key
from heydocker.functions import functions

logger = logging.getLogger(__name__)


def generate_gpt_functions(available_functions):
    """get all functions from functions.py"""
    python_obj_to_json_obj = {
        "str": "string",
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "list": "array",
        "dict": "object",
    }

    gpt_functions = []

    for function in available_functions:
        name = function.__name__
        docstring = inspect.getdoc(function)
        docstring_obj = parse(docstring)
        description = docstring_obj.short_description

        properties = {}
        for param in docstring_obj.params:
            param_name = param.arg_name
            param_type = param.type_name
            param_description = param.description

            properties[param_name] = {
                "type": python_obj_to_json_obj[param_type],
                "description": param_description,
            }

        gpt_functions.append(
            {
                "name": name,
                "description": description,
                "parameters": {"type": "object", "properties": properties},
            }
        )

    return gpt_functions


available_functions = [
    func
    for func in functions.__dict__.values()
    if callable(func) and func.__module__ == functions.__name__
]
gpt_functions = generate_gpt_functions(available_functions)


class GPTClient:
    def __init__(self):
        self.header = {
            "role": "system",
            "content": "You are a helpful assistant on a chat app. You can help user to monitor, remote, and control their docker server. Don't make assumptions about what values to use with functions. Ask for clarification if a user request is ambiguous. Always answer with human-readable text.",
        }
        self.history = []

    @property
    def messages(self):
        return [self.header] + self.history[-4:]

    def add_message(self, message):
        self.history.append(message)

    def handle_command(self, command):
        openai.api_key = get_openai_api_key()

        self.add_message(
            {
                "role": "user",
                "content": command,
            }
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=self.messages,
            functions=gpt_functions,
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
                messages=self.messages, model="gpt-3.5-turbo-0613"
            )

            self.add_message(
                {
                    "role": second_response["choices"][0]["message"]["role"],
                    "content": second_response["choices"][0]["message"]["content"],
                }
            )

            return second_response["choices"][0]["message"]["content"]

        else:
            self.add_message(
                {
                    "role": response_message["role"],
                    "content": response_message["content"],
                }
            )

            return response_message["content"]
