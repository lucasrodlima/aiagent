from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# Create a mapping of function names to their implementations
function_mapping = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call, verbose=False):

        match verbose:
            case True:
                print(f"Calling function: {function_call.name}({function_call.args})")
            case False:
                print(f"Calling function: {function_call.name}")
        
        function_call.args["working_directory"] = "./calculator"


        if function_call.name in function_mapping:

            result = function_mapping[function_call.name](**function_call.args)

            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result}
                    )
                ]
            )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={"error": f"Unknown function: {function_call.name}"}
                    )
                ]
            )

