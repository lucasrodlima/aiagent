import os

def write_file(working_directory, file_path, content):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.join(absolute_working_directory, file_path)

        if not absolute_file_path.startswith(absolute_working_directory):
            return f'Error: Cannot write to "{file_path}" outside of the working directory'

        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)

        with open(absolute_file_path, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'