import os
import sys

def get_python_files(directory):
  """Gets all python files in a directory and its subdirectories.

  Args:
    directory: The directory to search for python files.

  Returns:
    A list of paths to python files.
  """

  files = []
  for entry in os.listdir(directory):
    path = os.path.join(directory, entry)
    if os.path.isfile(path) and path.endswith(".py"):
      files.append(path)
    elif os.path.isdir(path):
      files.extend(get_python_files(path))
  return files

def print_python_file_info(files):
  """Prints the name and size of each python file.

  Args:
    files: A list of paths to python files.
  """

  for file in files:
    print(file, os.path.getsize(file))

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python print_python_files.py <directory>")
    sys.exit(1)

  directory = sys.argv[1]
  files = get_python_files(directory)
  print_python_file_info(files)
