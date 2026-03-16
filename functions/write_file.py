import os
from google import genai
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Provide the file path and the text to be written in said file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path",
            ),
            "content": types.Schema(
                type=types.Type.STRING, 
                description="Content to be written into the file"
            ),
        },
        required = ["file_path", "content"]
    ),
)




def write_file(working_directory, file_path, content):
    work_path = os.path.abspath(working_directory)
    target = os.path.normpath((os.path.join(work_path, file_path)))
    valid_dir = os.path.commonpath([work_path, target]) == work_path
    if os.path.isdir(target):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    if not valid_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    
    os.makedirs(os.path.dirname(target), exist_ok=True)

    try:
        with open(target, "w") as data:
            data.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"