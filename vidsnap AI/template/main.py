from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods= ["GET", "POST"])
def create():
    input_files = []
    myid = str(uuid.uuid1())
    if request.method == "POST":
        print("FILES:", request.files.keys())
        rec_id =(request.form.get("uuid"))
        desc = (request.form.get("text"))
        # rec_id check
        if not rec_id:
           rec_id = str(uuid.uuid1())
           print("UUID NHI MILA, NAYA BANAYA:", rec_id)
        for key, value in request.files.items():
            print(key, value)
            # Upload the file
            file = request.files[key]
            if file.filename == '':
               print("KHALI FILE SKIP")
               continue
        filename = secure_filename(file.filename)
        folder_path =(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
        os.makedirs(folder_path, exist_ok=True)
        save_path = (os.path.join(app.config['UPLOAD_FOLDER'], rec_id, filename))
        file.save(save_path)
        input_files.append(file.filename)
               # capture the description and save it to a file
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
                  f.write(desc or "")
    for fl in input_files:
         with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "a") as f:
              f.write(f"file '{fl}'\nduration 1\n")
              
    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

app.run(debug=True)