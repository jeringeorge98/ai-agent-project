
import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_files",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
               type= types.Type.ARRAY,
               items=types.Schema(type=types.Type.STRING),
               description= "Arguments to pass for the command" 
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory:str,file_path :str,args=None):
 try:
    working_dir_abs = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
    is_working_dir = os.path.commonpath([working_dir_abs,abs_file_path]) == working_dir_abs
    if is_working_dir is False :
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(abs_file_path) is False :
        return f'Error: "{file_path}" does not exist'

    if file_path.endswith(".py") is False :
        return f'Error: "{file_path}" is not a Python file'
    command = ["python",abs_file_path]

    if args :
        command.extend(args)
    output = ""    
    completed_process = subprocess.run(command,cwd= working_dir_abs , capture_output=True,timeout=30,text=True)
    #print(completed_process)
    if completed_process.returncode!= 0 :
        output = f'Process exited with code {completed_process.returncode}'
        return output
    elif completed_process.stdout == '' and completed_process.stderr == '':
        output = "No outputs produced"    
    elif completed_process.stdout:
        output = f'STDOUT: {completed_process.stdout}'
    elif completed_process.stderr:
        output = f'STDERR:{completed_process.stderr}'
    
        
    return output        


 except Exception as e :
    return f"Error: executing Python file: {e}"




