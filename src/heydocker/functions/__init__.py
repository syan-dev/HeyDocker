import inspect
import json
import logging

from docstring_parser import parse

from heydocker.functions import functions
from heydocker.functions.gpt import gpt_chat, gpt_function_calling

logger = logging.getLogger(__name__)

available_functions = [
    func
    for func in functions.__dict__.values()
    if callable(func) and func.__module__ == functions.__name__
]


def generate_functions_config():
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


functions_config = generate_functions_config()
logger.info("Function config generated.")
logger.info(json.dumps(functions_config, indent=4, sort_keys=True))
print(json.dumps(functions_config, indent=4, sort_keys=True))


def run(question: str):
    gpt_response = gpt_function_calling(question, functions_config)

    gpt_finish_response = gpt_response["choices"][0]["finish_reason"]
    gpt_message = gpt_response["choices"][0]["message"]

    if gpt_finish_response == "function_call":
        function_name = gpt_message["function_call"]["name"]
        function_arguments = gpt_message["function_call"]["arguments"]
        function_arguments = json.loads(function_arguments)
        logger.info(f"Function name: {function_name}")
        logger.info(f"Function arguments: {function_arguments}")
        command = f"functions.{function_name}(**{function_arguments})"
        try:
            data = eval(command)
            logger.info(f"Function data: {data}")
            response = gpt_chat(question, command, data)
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(e)
            response = gpt_chat(question, command, f"ERROR {e}")
            return response

    elif gpt_finish_response == "stop":
        return gpt_message["content"]

    else:
        return "Sorry, I can not process your request."
