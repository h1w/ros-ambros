import os
from flask import Flask, jsonify, request, redirect, url_for
from PIL import Image
import hashlib

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"msg": "Index page", "status": 200})

@app.route("/api/upload", methods=["POST"])
def process_image():
    file = request.files["image"]
    
    # Read the image via file.stream
    img = Image.open(file.stream)
    
    # Read payload from request
    payload = request.form.to_dict()
    name = payload["name"]
    description = payload["description"]
    gps = payload["gps"]

    # Push data to queue
    

    # Return json answer
    return jsonify({
        "msg": "success",
        "md5": {
            "name": hashlib.md5(name.encode("utf-8")).hexdigest(),
            "description": hashlib.md5(description.encode("utf-8")).hexdigest(),
            "gps": hashlib.md5(gps.encode("utf-8")).hexdigest()
        }
    })

# @app.route('/upload_file', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return 'there is no image in form'
#         image = request.files['image']
#         print(image)
#         return redirect(url_for('index'))
    
#     return '''
#     <h1>Upload new File</h1>
#     <form method="post" enctype="multipart/form-data">
#         <input type="file" name="image">
#         <input type="submit">
#     </form>
#     '''


#### App error handlers ####
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"msg": "Internal Server Error", "status": 500}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"msg": "Bad Request", "status": 400}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"msg": "Not Found", "status": 404}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10228, debug=False)