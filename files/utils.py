from werkzeug.exceptions import NotFound

#Doesn't check if names are unique
def get_file_from_filename(file_name, files):
    file = [file for file in files if file == file_name]
    if not file:
        raise NotFound('File was not found')
    return file[0]

def get_content_from_file(file, data_dir):
    with open(f'{data_dir}/{file}', 'r') as f: 
        file_content = f.readlines()
    return file_content
   
    