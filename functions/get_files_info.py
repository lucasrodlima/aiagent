import os

def get_files_info(working_directory, directory=None):

    try:
        allowed_root = os.path.abspath(working_directory)
        
        if directory == None:
            absolute_directory = allowed_root
        else:
            absolute_directory = os.path.abspath(os.path.join(allowed_root, directory))

        if not os.path.isdir(absolute_directory):
            return f'Error: "{directory}" is not a directory'
        elif not absolute_directory.startswith(allowed_root):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        contents = []
        for content in os.listdir(absolute_directory):
            content_path = os.path.join(absolute_directory, content)
            contents.append(f"- {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}")

        return "\n".join(contents) + "\n"
    except Exception as e:
        return f"Error: {e}"