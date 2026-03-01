from google.genai import types

from fuctions.get_files_content import schema_get_files_content
from fuctions.run_python_file import schema_run_python_file
from fuctions.write_file_content import schema_write_file_content
from fuctions.get_files_info import schema_get_files_info

available_functions = types.Tool(
    function_declarations=[schema_get_files_content,schema_run_python_file,schema_write_file_content],
)



def call_function(function_call, verbose=False):
    
    pass