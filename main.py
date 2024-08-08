import os
import inspect
import json
import subprocess


def list_files(directory, excluded_dirs=None, excluded_files=None, included_extension=None, excluded_extensions=None):
    """
    List all files in a directory, optionally excluding specified directories, specific files, and filtering by included and excluded file extensions.

    :param directory: The path of the directory to list files from.
    :param excluded_dirs: A list of directory names to exclude.
    :param excluded_files: A list of file names to exclude.
    :param included_extension: File extension to include.
    :param excluded_extensions: List of file extensions to exclude.
    :return: A list of file paths.
    """
    if excluded_dirs is None:
        excluded_dirs = []
    if excluded_files is None:
        excluded_files = []
    if included_extension is not None:
        included_extension = [ext.lower() for ext in included_extension]
    if excluded_extensions is None:
        excluded_extensions = []
    else:
        excluded_extensions = [ext.lower() for ext in excluded_extensions]

    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = file.split('.')[-1].lower()
            if (included_extension is None or file_ext in included_extension) and \
               (excluded_extensions is None or file_ext not in excluded_extensions) and \
               file not in excluded_files:
                file_list.append(file_path)

    return file_list

# Example usage
directory_path = ".\\"  # replace with your directory path
excluded_directories = ["venv", "__pycache__", ".idea", ".vscode", "JSON", "Cache", "Objects", ".git"]  # list of directories to exclude
excluded_files = ["interface_out.json", "__init__.py", "requirements.txt"]  # list of file names to exclude
included_extension = ["md", "py", "txt", "json", "lua"]  # file extension to include, set None to include all
# excluded_extensions = [".log", ".tmp", ".urdf", ".json", ".png", ".jpg", ".fbx"]  # list of file extensions to exclude
excluded_extensions = None # list of file extensions to exclude

files = list_files(directory_path, excluded_directories, excluded_files, included_extension)
print(files)

def generate_tree_map(directory, excluded_dirs=None, excluded_files=None, included_extension=None, excluded_extensions=None, prefix='', parent_prefix=''):
    """
    Generate a tree map of all files and directories in a directory, 
    mimicking the output of the 'tree' command in Linux.

    :param directory: The path of the directory to list files from.
    :param excluded_dirs: A list of directory names to exclude.
    :param excluded_files: A list of file names to exclude.
    :param included_extension: List of file extensions to include.
    :param excluded_extensions: List of file extensions to exclude.
    :param prefix: String prefix used for current level.
    :param parent_prefix: String prefix used for parent levels.
    :return: A string representing the tree map of the directory.
    """
    if excluded_dirs is None:
        excluded_dirs = []
    if excluded_files is None:
        excluded_files = []
    if included_extension is not None:
        included_extension = [ext.lower() for ext in included_extension]
    if excluded_extensions is None:
        excluded_extensions = []
    else:
        excluded_extensions = [ext.lower() for ext in excluded_extensions]

    tree_map = ''
    first_call = prefix == ''  # Check if it's the first call to avoid printing the root directory
    entries = os.listdir(directory)
    entries = [e for e in entries if e not in excluded_dirs and e not in excluded_files]
    entries_count = len(entries)

    for i, entry in enumerate(sorted(entries), start=1):
        entry_path = os.path.join(directory, entry)
        if os.path.isdir(entry_path):
            tree_map += f'{parent_prefix}{prefix}└── {entry}/\n' if i == entries_count else f'{parent_prefix}{prefix}├── {entry}/\n'
            if i == entries_count:
                sub_prefix = '    '
            else:
                sub_prefix = '│   '
            tree_map += generate_tree_map(entry_path, excluded_dirs, excluded_files, included_extension, excluded_extensions, prefix='├── ', parent_prefix=parent_prefix + sub_prefix)
        elif os.path.isfile(entry_path):
            file_ext = os.path.splitext(entry)[1].lower()
            if included_extension is None or file_ext in included_extension:
                if not (file_ext in excluded_extensions):
                    tree_map += f'{parent_prefix}{prefix}└── {entry}\n' if i == entries_count else f'{parent_prefix}{prefix}├── {entry}\n'

    if first_call:
        tree_map = f'{directory}/\n' + tree_map
    return tree_map

tree_map_string = generate_tree_map(directory_path, excluded_directories, excluded_files)
print(tree_map_string)


# import openai as client

# client.api_key = "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"


# supported_files = ['c', 'cpp', 'csv', 'docx', 'html', 'java', 'json', 'md', 'pdf', 'php', 'pptx', 'py', 'rb', 'tex', 'txt', 'css', 'jpeg', 'jpg', 'js', 'gif', 'png', 'tar', 'ts', 'xlsx', 'xml', 'zip']



def format_file_contents(file_paths):
    formatted_string = ""
    for path in file_paths:
        try:
            with open(path, 'r') as file:
                content = file.read()
                print(len(content), path)
                formatted_string += f'\n{path}\n```python\n{content}\n```\n'
        except FileNotFoundError:
            formatted_string += f'File not found: {path}\n'
    return formatted_string

# Example usage
formatted_output = format_file_contents(files)
print(formatted_output)
print(len(formatted_output))


def get_pip_freeze_output():
    try:
        # Run the pip freeze command and capture its output
        result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check for errors
        if result.stderr:
            print("Error:", result.stderr)
            return None

        # Return the output of pip freeze
        return result.stdout
    except FileNotFoundError:
        print("Error: pip not found")
        return None

# Usage
pip_freeze_output = get_pip_freeze_output()
if pip_freeze_output:
    print(pip_freeze_output)

def function_to_tool_spec(func):
    """
    Converts a Python function to a tool specification in JSON format.

    :param func: The function to convert.
    :return: A JSON string representing the tool specification.
    """
    spec = {
        'name': func.__name__,
        'description': func.__doc__.strip(),
        'parameters': {
            'type': 'object',
            'properties': {}
        },
        'required': []
    }

    # Extracting parameter information
    sig = inspect.signature(func)
    for name, param in sig.parameters.items():
        spec['parameters']['properties'][name] = {
            'description': f'The {name} number.',
            'type': 'number' if param.annotation in [int, float] else 'string'
        }
        if param.default is inspect.Parameter.empty:
            spec['required'].append(name)

    return json.dumps(spec, indent=4)


def update_file(file_path, content):
    """
    Updates the content of a file.
    """
    with open(file_path, 'w') as file:
        file.write(content)
        print(f'Updated {file_path}')
        
    return True

# Convert the function to a tool specification
tool_spec_json = function_to_tool_spec()
print(tool_spec_json)


context = """You're a coder, interacting with an existing project."""
context += "\n\nHere is the directory tree of the project :\n" + tree_map_string
context += "\n\nHere is the content of some of the files :\n" + formatted_output
context += "\n\nHere is the output of pip freeze :\n" + pip_freeze_output