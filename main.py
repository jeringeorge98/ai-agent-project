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
    
    get_files_info('calculator')
    # # user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=messages
    #     )
    # is_verbose = args.verbose
    # if response.usage_metadata is None:
    #     raise RuntimeError(f"Response failed with error")    
    # prompt_token_count = response.usage_metadata.prompt_token_count
    # response_token_count = response.usage_metadata.candidates_token_count
    # response_text = response.text

    # if is_verbose:
    #     print(f"User prompt:{args.user_prompt} \n Prompt tokens:{prompt_token_count}\n Response tokens:{response_token_count}\nResponse:{response_text}") 
    # else :
    #     print(f"Response : {response_text}")

       



if __name__ == "__main__":
    main()
