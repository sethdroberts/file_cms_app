from markdown import markdown

def convert_to_html(file):
    with open(file, 'r') as f:
        content = f.read()
    return markdown(content)