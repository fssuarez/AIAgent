import os
from pathlib import Path

def get_files_info(working_directory, directory="."):    
    work_path = os.path.abspath(working_directory)
    target = os.path.normpath((os.path.join(work_path, directory)))
    valid_dir = os.path.commonpath([work_path, target]) == work_path
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'
    
    if not valid_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        path = Path(target)
        folder_name = path.resolve().name
        if not folder_name:
            folder_name = directory
        header = f"Results for {folder_name} directory:"
        lines = [f"- {item.name}: file_size={item.stat().st_size} bytes, is_dir={item.is_dir()}" for item in Path(target).iterdir()]
        return header + "\n" + "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


