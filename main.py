import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
import time

verbose = True

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from aiagent!")

if __name__ == "__main__":
    main()

response = client.models.generate_content(
    model='gemini-2.5-flash', contents = messages, config = types.GenerateContentConfig(tools = [available_functions], system_instruction = system_prompt, temperature = 0)

)

if response:
    parts = response.candidates[0].content.parts
    function_calls = [part.function_call for part in parts if part.function_call]

    if function_calls:
        function_results = []
        for fc in function_calls:
            function_call_result = call_function(fc, verbose=True)
            if not function_call_result.parts:
                raise Exception("The result has no parts")
            if function_call_result.parts[0].function_response is None:
                raise Exception("The function response is none")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("The response field is none")
            
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f" -> {function_call_result.parts[0].function_response.response}")
            time.sleep(2)
        messages.append(types.Content(role="tool", parts=function_results))      
          
    else:
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    raise RuntimeError("No response")


