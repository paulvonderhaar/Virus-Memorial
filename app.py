import os
from flask import Flask, render_template, request, redirect, send_file
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import NoCredentialsError
import  psycopg2

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

class individual():
    def __init__(self,number,name):
        self.num=number
        self.name=name


def list_names():
    connection= psycopg2.connect(
    host = 'memorial.ccrcqb4iv5ys.us-east-1.rds.amazonaws.com',
    port = 5432,
    user = 'postgres',
    password='postgres',
    database='memorial'
    )

    cursor=connection.cursor()
    content=[]
    a=cursor.execute("Select * from memorial")
    b=cursor.fetchall()
    for i in range(len(b)): 
        temp=individual(b[i][0],b[i][1])
        content.append(temp)
    connection.commit()
    return(content)




def upload_file(file_name, file_id):
    access_key='AKIAQFSEYOHOTL5OCAYD'
    secret_key='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'
    s3 = boto3.client('s3',aws_access_key_id=access_key, aws_secret_access_key=secret_key)  

    try:
        file_name=file_name
        s3.upload_file(file_name,'memorialphotos', str(file_id)+".jpg")
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

@app.route('/list')
def memorial_list():
    content=list_names()
    return render_template('memorial_list.html',contents=content)

@app.route("/storage")
def storage():
    return render_template('storage.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        text = request.form['Name']
        connection= psycopg2.connect(
            host = 'memorial.ccrcqb4iv5ys.us-east-1.rds.amazonaws.com',
            port = 5432,
            user = 'postgres',
            password='postgres',
            database='memorial'
        )
        cursor=connection.cursor()
        cursor.execute("INSERT INTO memorial(name) VALUES (%s)",[text])

        connection.commit()

        a=cursor.execute("""select max(id) from memorial""")
        currentId=cursor.fetchall()
        connection.commit()



        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}",currentId[0][0])


        return redirect("/storage")

if __name__ == '__main__':
    app.run(debug=True)