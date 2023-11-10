import os

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
        included_extension = included_extension.lower()
    if excluded_extensions is None:
        excluded_extensions = []
    else:
        excluded_extensions = [ext.lower() for ext in excluded_extensions]

    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            if (included_extension is None or file_ext == included_extension) and \
               file_ext not in excluded_extensions and \
               file not in excluded_files:
                file_list.append(file_path)

    return file_list

# Example usage
directory_path = "./"  # replace with your directory path
excluded_directories = ["venv", "__pycache__", ".idea", ".vscode", "JSON", "Cache", "Objects", ".git"]  # list of directories to exclude
excluded_files = ["interface_out.json", "__init__.py"]  # list of file names to exclude
included_extension = None  # file extension to include, set None to include all
excluded_extensions = [".log", ".tmp", ".urdf", ".json"]  # list of file extensions to exclude

files = list_files(directory_path, excluded_directories, excluded_files, included_extension, excluded_extensions)
print(files)

import openai as client

client.api_key = "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"

assistant = client.beta.assistants.list().data[0]

supported_files = ['c', 'cpp', 'csv', 'docx', 'html', 'java', 'json', 'md', 'pdf', 'php', 'pptx', 'py', 'rb', 'tex', 'txt', 'css', 'jpeg', 'jpg', 'js', 'gif', 'png', 'tar', 'ts', 'xlsx', 'xml', 'zip']


# openai_files = []
# for file in files:
#     # Upload a file with an "assistants" purpose
    
#     if file.split('.')[-1] not in supported_files:
#         continue

#     print(os.path.abspath(file))
#     openai_files.append(
#         client.files.create(
#             file=open(os.path.abspath(file), "rb"),
#             purpose='assistants',
#             extra_headers={"source":file}
#         )
#     )

assistant = client.beta.assistants.create(
    name="Coder assistant",
    instructions="You are a coder assistant that have access to a specific codebase",
    tools=[{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id for file in client.files.list()]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What the library used in the main3D_ray.py ?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages)