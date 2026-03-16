import os
from pathlib import Path
from config import character_limit
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and provides the content of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path from which the content will be displayed.",
            ),
        },
        required = ["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    work_path = os.path.abspath(working_directory)
    target = os.path.normpath((os.path.join(work_path, file_path)))
    valid_dir = os.path.commonpath([work_path, target]) == work_path
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    if not valid_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(target, "r") as text:
            file_string = text.read(character_limit)

            if text.read(1):
                file_string += f'[...File "{target}" truncated at {character_limit} characters]'
        
        return file_string

    except Exception as e:
        return f"Error: {e}"
