import os
from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

messages = []
participants = set()  # מכיל את שמות כל המשתתפים
UPLOAD_FOLDER = os.path.abspath("uploads")
GROUP_NAME = "Chat Group"  # שם הקבוצה

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        file = request.files.get('file')
        if username and message:
            participants.add(username)  # הוסף את שם המשתמש לרשימת המשתתפים
            if file:
                file_name = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                file.save(file_path)
                messages.append({'username': username, 'message': message, 'file': file_name})
            else:
                messages.append({'username': username, 'message': message, 'file': None})
    return render_template('chat.html', messages=messages, group_name=GROUP_NAME, participants=participants)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
