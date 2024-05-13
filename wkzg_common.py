import glob
import pathlib

def get_file_extension(filepath: str):
    return pathlib.Path(filepath).suffix

def get_file_content(filepath: str):
    with open(filepath, 'r') as file:
        content = file.read()
        return content
    return ""

def save_file_content(filepath: str, fileContent: str):
    with open(filepath, 'w') as file:
        file.write(fileContent)

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]