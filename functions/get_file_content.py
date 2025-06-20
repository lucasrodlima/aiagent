import os
def get_file_content(working_directory, file_path):
    try:
        allowed_root = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(allowed_root, file_path))

        if not absolute_file_path.startswith(allowed_root):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(absolute_file_path):
            return f"Error: File not found or is not a regular file: {file_path}"

        MAX_CHARS = 10000 
        file_content_string = ""

        with open(absolute_file_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) >= MAX_CHARS:
            file_content_string += f"\n\n[... File {file_path} truncated, file exceeds 10,000 characters]"
    
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
