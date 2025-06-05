from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
@app.route('/submit', methods=['GET', 'POST'])
def submit_paper():
    if request.method == 'POST':
        data = {
            'student_name': request.form['student_name'],
            'student_id': request.form['student_id'],
            'email': request.form['email'],
            'college': request.form['college'],
            'stream': request.form['stream'],
            'course': request.form['course'],
            'title': request.form['title'],
            'abstract': request.form['abstract'],
            'doc_link': request.form.get('doc_link', '')
        }

        file = request.files.get('doc_upload')
        if file and file.filename:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            data['doc_upload'] = filepath
        else:
            data['doc_upload'] = ''

        with open('submissions.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        return render_template("success.html", name=data['student_name'])

    return render_template("sumbit_paper.html")


@app.route('/view', methods=['GET', 'POST'])
def view_submission():
    submissions = []
    if request.method == 'POST':
        email = request.form['email']
        if os.path.exists('submissions.csv'):
            with open('submissions.csv', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                submissions = [row for row in reader if row['email'] == email]
    return render_template("view_submission.html", submissions=submissions)


if __name__ == '__main__':
    app.run(debug=True)
