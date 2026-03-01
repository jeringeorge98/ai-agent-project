from google.genai import types
from config import MAX_CHARS
from os import read
import os

schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Read the contents of the file.First check if the file is in the permitted workign directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file we need to read contents from.",
            ),
        },
        required=["file_path"]
    ),
)
def get_file_content(working_directory,file_path) -> str:
    
    try:
     #get absolute path
     working_dir_abs = os.path.abspath(working_directory)
     file_content =""
     #join path names
     if os.path.isfile(file_path) is None:
        return f'Error: "{file_path}" is not a file'
     target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

     is_valid_target_dir = os.path.commonpath([working_dir_abs,target_dir]) == working_dir_abs
    #  print(target_dir,working_dir_abs)
    #  print(is_valid_target_dir,"Is Valid target")
     if is_valid_target_dir is False:
        return f'Error: Cannot read {file_path} as it is outside the permitted working directory.'

     #Read the file
     print(file_path,working_dir_abs,working_directory)
     file_path = os.path.join(working_directory,file_path)
     with open(file_path,"r") as f:
        file_content = f.read(MAX_CHARS)
        if f.read(1):
            file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
     return file_content 
         

    except Exception as e:
        return f'Error:Eroor getting file content with exception {e}'    