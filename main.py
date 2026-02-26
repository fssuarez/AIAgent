import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
