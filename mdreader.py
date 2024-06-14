from flask import Flask, render_template, send_from_directory
import os
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from pygments.formatters.html import HtmlFormatter


app = Flask(__name__)
app.config['MARKDOWN_FOLDER'] = 'md/typora'

# @app.route('/')
# def index():
#     files = os.listdir(app.config['MARKDOWN_FOLDER'])
#     markdown_files = [f for f in files if f.endswith('.md')]
#     return render_template('index.html', files=markdown_files)

def get_markdown_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.relpath(os.path.join(root, file), directory))
    return md_files

@app.route('/')
def index():
    files = get_markdown_files(app.config['MARKDOWN_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/read/<path:filename>')
def read_file(filename):
    if not filename.endswith('.md'):
        return "Invalid file type", 400
    filepath = os.path.join(app.config['MARKDOWN_FOLDER'], filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        html_content = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        html_content = html_content.replace('src="assets/', 'src="/typora/assets/')
    formatter = HtmlFormatter(style='vs')
    # formatter = HtmlFormatter(style='pastie')

    # formatter = HtmlFormatter(style='manni')
    formatter = HtmlFormatter(style='nord')
    light_formatter = HtmlFormatter(style='vs')
    dark_formatter = HtmlFormatter(style='nord')

    light_css_string = light_formatter.get_style_defs('.codehilite')
    dark_css_string = dark_formatter.get_style_defs('.codehilite')

    css_string = formatter.get_style_defs('.codehilite')
    return render_template('index.html', content=html_content, light_css_string=light_css_string, dark_css_string=dark_css_string)

@app.route('/typora/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(app.config['MARKDOWN_FOLDER'], 'assets'), filename)



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port='1995', debug= True)

