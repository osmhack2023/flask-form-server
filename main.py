import os
import csv
import requests
from datetime import datetime
from uuid import uuid4
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/submit/',methods=['POST'])
def submit():
    print(request.form)
    if not request.form.get('token'):
        return {"success" : False, "message": "empty token"}
    token = request.form['token']
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_secret_key = os.getenv("SECRET_KEY")
    payload = {
       'secret': recaptcha_secret_key,
       'response': token,
       'remoteip': request.remote_addr,
    }
    response = requests.post(recaptcha_url, data = payload)
    success = response.json().get('success', False)
    result = {"success" : success, "message": "Captcha verification failed, try again!" if not success else ""}
    print(result, response.json())
    return result

@app.route('/api/formsubmit/', methods=['POST'])
def formSubmit():
    print(request.files)
    print(request.form)
    data = request.form.to_dict()
    try:
        file = request.files['file'] 
        filename = secure_filename(file.filename)
        uid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        filename_uid = uid + "_" + filename[-100:]
        destination=f"{UPLOAD_FOLDER}/{filename_uid}"
        file.save(destination)
        SITE_URL = os.getenv("SITE_URL")
        append_to_csv(data, f'{SITE_URL}/{filename_uid}')
        return {'success':True, 'message': ''}
    except Exception as e:
        print(e)
        return {'success':False, 'message': str(e)}

def append_to_csv(data, file_url):
    fieldnames = ["name","email","phone_number","address","college_name","team_name","short_description","member1_name","member1_email","member1_phone","member1_github","member1_vegornonveg","member1_size","member2_name","member2_email","member2_phone","member2_github","member2_vegornonveg","member2_size","member3_name","member3_email","member3_phone","member3_github","member3_vegornonveg","member3_size","member4_name","member4_email","member4_phone","member4_github","member4_vegornonveg","member4_size","project_name","project_description","url","timestamp"]

    with open(f'{UPLOAD_FOLDER}/data.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        ordered_data = {key: data[key] for key in fieldnames if key in data}  # Preserve the order of fieldnames in data

        # Fill in missing fields with empty strings
        for key in fieldnames:
            if key not in ordered_data:
                ordered_data[key] = ''

        ordered_data['url'] = file_url
        ordered_data['timestamp'] = datetime.now().strftime('%Y-%m-%d%H-%M%S')
        writer.writerow(ordered_data)

if __name__ == "__main__":
    app.run(port=9000)
