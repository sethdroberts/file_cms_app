from flask import (
    Flask, 
    render_template, 
    send_from_directory, 
    flash, 
    redirect, 
    url_for
    )
    
from functools import wraps
import os
from files.utils import convert_to_html

app = Flask(__name__)
app.secret_key = 'secret1'

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
@require_data_dir
def get_file(data_dir, file_name):
    filepath = os.path.join(data_dir, file_name)
    if os.path.isfile(filepath):
        if file_name.endswith(".md"):
            return convert_to_html(filepath)
        else:
            return send_from_directory(data_dir, file_name)
    else:
        flash(f'{file_name} does not exist', 'error')
        return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)