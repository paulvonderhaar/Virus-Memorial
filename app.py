import os
import inspect
import boto3
import psycopg2
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/submit/",methods=['POST'])
def chart():
    file=request.files("input_image")
    access_key='AKIAQFSEYOHOTL5OCAYD'
    secret_key='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'
    s3 = boto3.client('s3',aws_access_key_id=access_key, aws_secret_access_key=secret_key)  
    try:
        s3.upload_file(file,'memorialphotos','test.jpg')
        return "True"
    except FileNotFoundError:
        print("The file was not found")
        return "False"
    except NoCredentialsError:
        print("Credentials not available")
        return "False"





if __name__ == "__main__":
    app.run()
