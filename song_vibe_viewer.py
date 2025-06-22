from flask import Flask, render_template_string
import os

app = Flask(__name__)

# HTML template with syntax highlighting
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Song Vibe Python Code Viewer</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #1e1e1e;
            color: #d4d4d4;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #252526;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        h1 {
            color: #569cd6;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #569cd6;
            padding-bottom: 10px;
        }
        .code-container {
            background: #1e1e1e;
            border-radius: 6px;
            padding: 20px;
            overflow-x: auto;
            border: 1px solid #3c3c3c;
        }
        .line-numbers {
            display: inline-block;
            width: 50px;
            color: #858585;
            text-align: right;
            margin-right: 20px;
            user-select: none;
        }
        .code-line {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .string { color: #ce9178; }
        .keyword { color: #569cd6; }
        .comment { color: #6a9955; }
        .function { color: #dcdcaa; }
        .number { color: #b5cea8; }
        .operator { color: #d4d4d4; }
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #569cd6;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            font-family: Arial, sans-serif;
        }
        .back-to-top:hover {
            background: #4a8bc7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Song Vibe Python Code Viewer</h1>
        <div class="code-container">
            {{ code_html | safe }}
        </div>
    </div>
    <a href="#" class="back-to-top" onclick="window.scrollTo(0,0)">↑ Top</a>
</body>
</html>
"""

def highlight_python_code(code):
    """Simple Python syntax highlighting"""
    import re
    
    # Keywords
    keywords = ['import', 'from', 'def', 'class', 'if', 'else', 'elif', 'for', 'while', 
               'try', 'except', 'finally', 'with', 'as', 'return', 'yield', 'break', 
               'continue', 'pass', 'raise', 'True', 'False', 'None', 'and', 'or', 'not',
               'in', 'is', 'lambda', 'global', 'nonlocal', 'del', 'assert']
    
    # String patterns
    code = re.sub(r'("""[\s\S]*?""")', r'<span class="string">\1</span>', code)
    code = re.sub(r'(".*?")', r'<span class="string">\1</span>', code)
    code = re.sub(r"('.*?')", r'<span class="string">\1</span>', code)
    
    # Comments
    code = re.sub(r'(#.*?)$', r'<span class="comment">\1</span>', code, flags=re.MULTILINE)
    
    # Keywords
    for keyword in keywords:
        code = re.sub(r'\b' + keyword + r'\b', r'<span class="keyword">\g<0></span>', code)
    
    # Function definitions
    code = re.sub(r'\bdef\s+(\w+)', r'<span class="keyword">def</span> <span class="function">\1</span>', code)
    
    # Numbers
    code = re.sub(r'\b(\d+)\b', r'<span class="number">\1</span>', code)
    
    return code

@app.route('/')
def view_code():
    try:
        with open('ai_native broomes/song_vibe.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Add line numbers and highlight syntax
        lines = code.split('\n')
        highlighted_lines = []
        
        for i, line in enumerate(lines, 1):
            highlighted_line = highlight_python_code(line)
            highlighted_lines.append(f'<span class="line-numbers">{i:3d}</span><span class="code-line">{highlighted_line}</span>')
        
        code_html = '\n'.join(highlighted_lines)
        
        return render_template_string(HTML_TEMPLATE, code_html=code_html)
    
    except FileNotFoundError:
        return "Error: song_vibe.py file not found!", 404
    except Exception as e:
        return f"Error reading file: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5003) 