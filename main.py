import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.call_function import call_function

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        sys.exit("Error: GEMINI_API_KEY not found in environment variables")

    client = genai.Client(api_key=api_key)

    # Create a mapping of function names to their implementations
    function_mapping = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file in the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info,
                            schema_get_file_content,
                            schema_run_python_file,
                            schema_write_file]
    )

    # Check if the user provided a prompt
    try:
        if len(sys.argv) < 2:
            sys.exit("Error: no prompt")
        user_prompt = sys.argv[1]
    except Exception as e:
        sys.exit(f"Error parsing command-line arguments: {str(e)}")

    # Prepare the messages for the Gemini API
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for i in range (20):
        try:
            client_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                )
            )
        except Exception as e:
            sys.exit(f"Error calling Gemini API: {str(e)}")

        # Add response candidates to messages
        for candidate in client_response.candidates:
            messages.append(candidate.content)

        conversation_complete = False

        # Iterate over function calls
        if client_response.function_calls:
            for function_call in client_response.function_calls:
                verbose = False

                if "--verbose" in sys.argv:
                    verbose = True

                result = call_function(function_call, verbose=verbose)
                if result.parts[0].function_response.response:
                    print(f"--> {result.parts[0].function_response.response}")
                else:
                    print(f"--> Error: {result.parts[0].function_response.error}")

                # Add types.Content/result to messages
                messages.append(result)
        else:
            print(client_response.text)
            conversation_complete= True
            break

        # Handle verbose mode
        if "--verbose" in sys.argv:
            print(f"User prompt: {user_prompt}")
            if hasattr(client_response, 'usage_metadata'):
                print(f"Prompt tokens: {client_response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {client_response.usage_metadata.candidates_token_count}")
            else:
                print("Usage metadata not available")

        if conversation_complete:
            break


if __name__ == "__main__":
    main()
    sys.exit(0)
# End of main.py