from flask import (
    Flask, 
    render_template, 
    send_from_directory, 
    flash, 
    redirect, 
    request,
    session,
    url_for
    )
    
from functools import wraps
import os
from files.utils import (
    convert_to_html,
    correct_credentials,
    create_new_file,
    get_content_from_file, 
    replace_file_content
    )

app = Flask(__name__)
app.secret_key = 'secret1'

def get_data_path():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'data')
    else:
        return os.path.join(os.path.dirname(__file__), 'cms', 'data')

def require_files(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data_dir = get_data_path()
        files = [os.path.basename(path) for path in os.listdir(data_dir)]
        return f(files=files, *args, **kwargs)

    return decorated_function
    
def require_data_dir(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data_dir = get_data_path()
        return f(data_dir=data_dir, *args, **kwargs)

    return decorated_function
    
def require_sign_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session['username']:
                return f(*args, **kwargs)
        except KeyError:
            flash('You must be signed in to view this page', 'error')
            return redirect(url_for('sign_in'))

    return decorated_function

@app.route("/")
@require_files
@require_sign_in
def index(files):
    return render_template('files.html', files=files)
    
@app.route('/files/<file_name>')
@require_data_dir
@require_sign_in
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
        
@app.route('/files/<file_name>/edit')
@require_data_dir
@require_sign_in
def edit_file(data_dir, file_name):
    file_content = get_content_from_file(file_name=file_name, data_dir=data_dir)
    return render_template('edit_file.html', file_name=file_name, file_content=file_content)
    
@app.route('/files/<file_name>', methods=['POST'])
@require_data_dir
def save_edits(data_dir, file_name):
    new_file_content = request.form['file_text']
    replace_file_content(new_file_content=new_file_content, file_name=file_name, data_dir=data_dir)
    flash(f'{file_name} has been updated.', 'success')
    return redirect(url_for('index'))
    
@app.route('/files/new')
@require_sign_in
def create_file():
    return render_template('create_file.html')
    
@app.route('/files/new', methods=["POST"])
@require_data_dir
def save_file(data_dir):
    file_name = request.form['file_name']
    file_path = os.path.join(data_dir, file_name)
    
    if not file_name:
        flash('A name is required', 'error')
        return render_template('create_file.html')
    elif not (file_name.endswith(".md") or file_name.endswith(".txt")):
        flash("File must end with a 'txt' or 'md' extension.")
        return render_template('create_file.html')
    elif os.path.exists(file_path):
        flash(f'{file_name} already exists', 'error')
        return render_template('create_file.html')
    else:
        create_new_file(file_name=file_name, data_dir=data_dir)
        flash(f'{file_name} was created.')
        return redirect(url_for('index'))
    
@app.route('/files/<file_name>/delete')
@require_sign_in
@require_data_dir
def delete_file(data_dir, file_name):
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"{file_name} has been deleted", 'success')
        return redirect(url_for('index'))
    else:
        flash(f"{file_name} doesn't exist", 'error')
        return redirect(url_for('index'))

@app.route('/sign-in/')
def show_sign_in():
    return render_template('sign_in.html')
    
@app.route('/sign-in/', methods=['POST'])
def sign_in():
    username = request.form['username']
    password = request.form['password']
    credential_path = os.path.join(os.path.dirname(__file__), 'cms', 'users.yml')
    if correct_credentials(username, password, credential_path):
        session['username'] = username
        flash('Welcome!', 'success')
        return redirect(url_for('index'))
    flash('Invalid credentials', 'error')
    return render_template('sign_in.html')
    
@app.route('/sign-out/', methods=["POST"])
@require_sign_in
def sign_out():
    session.pop('username', None)
    flash('You have been signed out')
    return redirect(url_for('sign_in'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)