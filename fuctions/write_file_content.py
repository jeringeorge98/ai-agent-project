
import os
def write_file_content(working_dir, file_path,content):
    try:
    #Acess check
     working_dir_abs = os.path.abspath(working_dir)
    
     abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
     is_valid_target_dir = os.path.commonpath([working_dir_abs,abs_file_path]) == working_dir_abs
     if is_valid_target_dir is False :
        return f'Error: Cannot read {file_path} as it is outside the permitted working directory.'
     if os.path.isdir(abs_file_path):
        return f'Error : {file_path} is not a file but a directory'

     print(file_path,working_dir,abs_file_path)
     os.makedirs(exist_ok=True,name= os.path.dirname(abs_file_path))
     with open(abs_file_path,'w') as f:
        f.write(content)
     return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'   
    except Exception as e :
        return f'Error: Error while writing to file with exception {e}' 


