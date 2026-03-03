from call_functions import call_function
from call_functions import available_functions
from fuctions.prompts.prompts import system_prompt
from fuctions.get_files_content import get_file_content
from fuctions.get_files_info import get_files_info
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key= api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

if api_key is None:
    raise RuntimeError("No Api key available")

def main():
    
    #get_files_info('calculator')
    #get_file_content('calculator',"lerm_ipsum.txt")
    # user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config= types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions])
        )
    is_verbose = args.verbose
    if response.usage_metadata is None:
        raise RuntimeError(f"Response failed with error")    
    prompt_token_count = response.usage_metadata.prompt_token_count
    response_token_count = response.usage_metadata.candidates_token_count
    response_text = response.text
    function_calls = response.function_calls
    results = []
    if function_calls is None : 
     if is_verbose:
        print(f"User prompt:{args.user_prompt} \n Prompt tokens:{prompt_token_count}\n Response tokens:{response_token_count}\nResponse:{response_text}") 
     else :
        print(f"Response : {response_text}")
    else :
        for fnc in function_calls :
            function_call_result = call_function(fnc,is_verbose)
            if function_call_result.parts is None or function_call_result.parts[0] is None : 
                raise Exception(f"Function call result is empty")
            final_response = function_call_result.parts[0].function_response.response

            if final_response is None :
                raise Exception(f"Final response is None")

            results.append(function_call_result.parts[0])
            if is_verbose :
                print(f"-> {function_call_result.parts[0].function_response.response}")   
  except Exception as e :
    print(f"Error with Exception {e}")

       



if __name__ == "__main__":
    main()
