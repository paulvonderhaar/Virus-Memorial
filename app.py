import os
from flask import Flask, render_template, request, redirect, send_file
import boto3
app = Flask(__name__)
def upload_file(file_name):
    access_key='AKIAQFSEYOHOTL5OCAYD'
    secret_key='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'
    s3 = boto3.client('s3',aws_access_key_id=access_key, aws_secret_access_key=secret_key)  

    try:
        file_name=file_name
        s3.upload_file(file_name,'memorialphotos','0000001.jpg')
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route("/storage")
def storage():
    return render_template('storage.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        upload_file(f.filename)

        return redirect("/storage")

if __name__ == '__main__':
    app.run(debug=True)