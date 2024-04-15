import os
from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='index_templates')

messages = []
participants = set()  # מכיל את שמות כל המשתתפים
UPLOAD_FOLDER = os.path.abspath("uploads")
GROUP_NAME = "Chat Group"  # שם הקבוצה

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def chat():
    global username
    global message
    if request.method == 'POST':


        username = request.form.get('username')  # קריאה ל-request.form.get() כדי לקבל את הערך של 'username'
        message = request.form.get('message')  # קריאה ל-request.form.get() כדי לקבל את הערך של 'message'
        file = request.files.get('file')  # קבלת הקובץ מהבקשה

        if username and message:
            participants.add(username)  # הוספת שם משתמש לרשימת המשתתפים

            if file:  # אם קיבלנו קובץ מהבקשה
                file_name = secure_filename(file.filename)  # שמירת שם הקובץ בצורה בטוחה
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)  # יצירת נתיב לשמירת הקובץ
                file.save(file_path)  # שמירת הקובץ בנתיב המתאים
                messages.append({'username': username, 'message': message, 'file': file_name})  # הוספת הודעה לרשימת ההודעות עם פרטי המשתמש והקובץ
            else:
                messages.append({'username': username, 'message': message, 'file': None})  # הוספת הודעה לרשימת ההודעות בלעדי קובץ

    return render_template('index.html', messages=messages, group_name=GROUP_NAME, participants=participants)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




if __name__ == '__main__':
    app.run(debug=True)
