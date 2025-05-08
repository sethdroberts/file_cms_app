from markdown import markdown
import os
import yaml
import bcrypt

def convert_to_html(file):
    with open(file, 'r') as f:
        content = f.read()
    return markdown(content)
    
def get_content_from_file(file_name, data_dir):
    with open(f'{data_dir}/{file_name}', 'r') as f: 
        file_content = f.read()
    return file_content
    
def replace_file_content(new_file_content, file_name, data_dir):
    with open(f'{data_dir}/{file_name}', 'r+') as f:
        f.truncate(0)
        f.write(new_file_content)
    return

def create_new_file(file_name, data_dir):
    filepath = os.path.join(data_dir, file_name)
    f = open(filepath, "a")
    f.close()
    
def correct_credentials(username, password, filepath):
    with open(filepath, 'r') as f:
        file_content = yaml.safe_load(f)
    if file_content.get(username, False):
        hashed_pw = file_content.get(username).encode('utf-8')
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_pw)
    return False
