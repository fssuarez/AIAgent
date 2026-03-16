import os
import subprocess
from google import genai
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python program at a specified path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items = types.Schema(type = types.Type.STRING), 
                description="Optional list of arguments"
            ),
        },
        required = ["file_path"]
    ),
)


def run_python_file(working_directory, file_path, args=None):
    work_path = os.path.abspath(working_directory)
    target = os.path.normpath((os.path.join(work_path, file_path)))
    valid_dir = os.path.commonpath([work_path, target]) == work_path
    
    if not valid_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target):
        return f'Error: "{file_path}" does not exist or is not a regular file' 
    
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target]
    if args:
        command.extend(args)


    try:
        Process = subprocess.run(command, cwd = work_path, capture_output = True, text = True, timeout = 30)
        output_parts = []

        if Process.returncode != 0:
            output_parts.append(f"Process exited with code {Process.returncode}")

        if not Process.stderr and not Process.stdout:
            output_parts.append(f"No output produced")

        if Process.stderr:
            output_parts.append(f"STDERR:\n{Process.stderr}")
        
        if Process.stdout:
            output_parts.append(f"STDOUT:\n{Process.stdout}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: {e}"
