import os 
import argparse
from dotenv import load_dotenv
from openai import OpenAI



def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("no api key found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,

    )
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]

    user_prompting = args.user_prompt
    verbosity = args.verbose 


    generate_content(client, messages, verbosity, user_prompting)

    
    
def generate_content(
    client: OpenAI, 
    messages: list, 
    verbosity: bool,
    user_prompting: str
    ) -> None:
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )
    if response.usage == None:
            raise RuntimeError("no usage as occurred")
    if verbosity == True:
        print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
        print(f"User prompt: {user_prompting}")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
