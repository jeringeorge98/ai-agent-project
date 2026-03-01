from google.genai import types
from fuctions.get_files_content import schema_get_files_content
from fuctions.run_python_file import schema_run_python_file
from fuctions.write_file_content import schema_write_file_content

available_functions = types.Tool(
    function_declarations=[schema_get_files_content,schema_run_python_file,schema_write_file_content],
)



def call_function(function_call : types.FunctionCall, verbose=False):
    
    if verbose :
        print(f"Calling function: {function_call.name}({function_call.args})")
    else :
        print(f" - Calling function: {function_call.name}")

