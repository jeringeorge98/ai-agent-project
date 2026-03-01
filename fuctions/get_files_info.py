
from typing import AnyStr
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory=".")->str:
    try:

     #get absolute path
     working_dir_abs = os.path.abspath(working_directory)
     #join path names
     if os.path.isdir(directory) is None:
        return f'Error: "{directory}" is not a directory'
     target_dir:AnyStr = os.path.normpath(os.path.join(working_dir_abs, directory))

     is_valid_target_dir = os.path.commonpath([working_dir_abs,target_dir]) == working_dir_abs
    #  print(target_dir,working_dir_abs)
    #  print(is_valid_target_dir,"Is Valid target")
     if is_valid_target_dir is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

     #iterate over items in taget_drir
     items = os.listdir(target_dir)
    
     formatted_items=[]
     for item in items:
        filepath = os.path.join(target_dir,item)
        is_dir = os.path.isdir(filepath)
        size = os.path.getsize(filepath)
        #print(is_dir,size,item)
        formatted_items.append(f'-{item}: file_size={size} bytes, is_dir={is_dir}')
        
    # print(formatted_items)
     result='\n'.join(formatted_items)
    #  print(result)
     return result
    except Exception as e:
        return f'Error listing files:{err}'      
   






