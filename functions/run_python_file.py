import subprocess
import os
def run_python_file(working_directory, file_path):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'
    
    elif not os.path.isfile(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    
    elif not absolute_file_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file'
    
    try:
        result = subprocess.run(
            ['python', absolute_file_path],
            timeout=30,
            cwd=absolute_working_directory,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'

        if not result.stdout and not result.stderr:
            return 'No output produced'

        return f'STDOUT:\n{result.stdout.strip()}\n' \
               f'STDERR:\n{result.stderr.strip()}'

    except Exception as e:
        return f'Error: executing python file: {str(e)}'
