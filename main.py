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
    try:
        conversation_messages = messages.copy()  # Start with initial user prompt
        
        for iteration in range(20):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation_messages,
                config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
            )
            
            is_verbose = args.verbose
            if response.usage_metadata is None:
                raise RuntimeError(f"Response failed with error")
            
            # Add model's response to conversation history
            if response.candidates:
                for candidate in response.candidates:
                    conversation_messages.append(candidate.content)
            
            prompt_token_count = response.usage_metadata.prompt_token_count
            response_token_count = response.usage_metadata.candidates_token_count
            response_text = response.text
            function_calls = response.function_calls
            
            # Check if model has final response (no function calls)
            if function_calls is None:
                if is_verbose:
                    print(f"Final response:\n{response_text}")
                    print(f"User prompt: {args.user_prompt}")
                    print(f"Prompt tokens: {prompt_token_count}")
                    print(f"Response tokens: {response_token_count}")
                else:
                    print(f"Final response:\n{response_text}")
                return  # Exit successfully
            
            # Handle function calls
            function_responses = []
            for fnc in function_calls:
                if is_verbose:
                    print(f" - Calling function: {fnc.name}")
                
                function_call_result = call_function(fnc, is_verbose)
                if function_call_result.parts is None or function_call_result.parts[0] is None:
                    raise Exception(f"Function call result is empty")
                
                function_responses.append(function_call_result.parts[0])
            
            # Add function results to conversation history
            conversation_messages.append(types.Content(role="user", parts=function_responses))
        
        # If we reach here, max iterations exceeded
        print("Error: Maximum iterations reached without final response. The agent may be stuck in a loop.")
        exit(1)
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

       



if __name__ == "__main__":
    main()
