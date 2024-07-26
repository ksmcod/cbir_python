from flask import Flask, render_template,request
import os
import shutil
from functions import retrieve_images

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['FEATURES_FOLDER'] = 'features/'
# app.config['STATIC_FOLDER'] = 'static/uploads/'

@app.route("/")
def index():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        except Exception as e:
            print(f"Failed to delete {file_path}. Error: {e}")

    return render_template("index.html")

@app.route("/results",methods=['POST'])
def results():
    if request.method == 'POST':
        try: 
            # Save query image
            query_image = request.files['query']
            query_image_path = os.path.join(app.config['UPLOAD_FOLDER'], query_image.filename)
            query_image.save(query_image_path)

            # Save database images
            database = request.files.getlist("database")
            db_paths = []

            for image in database:
                db_image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(db_image_path)
                db_paths.append(db_image_path)

            results =  retrieve_images(query_image_path)

            result_images = []

            for item in results:
                image_path = f"static/uploads/{item[0]}"
                result_images.append(image_path)
            
            print(result_images)
            print(query_image_path)

            return render_template("results.html",image=query_image_path,results=result_images)
            
        
        except Exception as e:
            print(e)



app.run(debug=True)