from flask import Flask, render_template
from functools import wraps
import os
from files.utils import (
    get_content_from_file,
    get_file_from_filename,
    )

app = Flask(__name__)

def require_files(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        root = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(root, "cms", "data")
        files = [os.path.basename(path) for path in os.listdir(data_dir)]
        return f(files=files, *args, **kwargs)

    return decorated_function
    
def require_data_dir(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        root = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(root, "cms", "data")
        return f(data_dir=data_dir, *args, **kwargs)

    return decorated_function

@app.route("/")
@require_files
def index(files):
    return render_template('files.html', files=files)
    
@app.route('/files/<file_name>')
@require_files
@require_data_dir
def get_file(files, data_dir, file_name):
    #Doesn't check if names are unique and raises NotFound
    file = get_file_from_filename(file_name, files)
    file_content = get_content_from_file(file, data_dir)
    return render_template('file.html', file_content=file_content)
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)