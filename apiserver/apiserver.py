import os
from flask import Flask, jsonify, request, redirect, url_for
from PIL import Image
import hashlib
import psycopg2
import datetime
from pathlib import Path
from base64 import decodestring
import json

# ambros neural network
from keras.preprocessing import image as keras_image
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
# import tensorflow as tf
from tensorflow.keras.models import load_model
import requests
import base64

model = load_model('/home/frizik/SfeduNET_4.0/my_h5_model.h5')

def validate_single(img_path):
    img = keras_image.load_img(img_path, target_size=(200,200))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    result = False
    if classes[0] < 0.5:
        # Ambrosia
        result = True
    else:
        # Not ambrosia
        result = False
    return result

def push_marker_to_map(name, description, gps, img_path):
    url = "http://localhost:8000/map/api/upload"

    name = "app"
    description = "Ragweed"
    gps = "{}, {}".format(gps.split(' ')[1], gps.split(' ')[0])

    img = Image.open(img_path)
    img.save(img_path, quality=70, optimize=True)
    img = open(img_path, "rb").read()
    img_64_encode = base64.encodebytes(img).decode()
    payload = {
        "name": name,
        "description": description,
        "gps": gps,
        "image": img_64_encode,
        "request_type": "ambros",
    }

    # print(name)
    # print(description)
    # print(gps)

    response = requests.post(url, data=payload, verify=False)
    return response

# Constants
CLIENT_PATH = "/var/www/html/rosambros/clients/images"
REPOSITORY_DIR = Path(__file__).resolve().parent.parent

# Import credentials module contains secret data
from importlib.machinery import SourceFileLoader
secret_credentials = SourceFileLoader('module.secret_credentials', '{}/secret_credentials.py'.format(REPOSITORY_DIR)).load_module()


# Postgresql section
def rosambrosdb_insert_client(client_data):
    # Insert a new client into the clients table
    sql = """INSERT INTO client (img, name, description, gps) VALUES(%s, %s, %s, %s)"""
    conn = None
    client_id = None

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=secret_credentials.database["rosambrosdb"]["HOST"],
            database=secret_credentials.database["rosambrosdb"]["NAME"],
            user=secret_credentials.database["rosambrosdb"]["USER"],
            password=secret_credentials.database["rosambrosdb"]["PASSWORD"],
            port=secret_credentials.database["rosambrosdb"]["PORT"]
        )
        
        # Create a new cursor
        cur = conn.cursor()
        
        # Execute the INSERT statement
        cur.execute(sql, (client_data['img'],client_data['name'],client_data['description'],client_data['gps'],))
        
        # Commit the changes to the database
        conn.commit()
        
        count = cur.rowcount
        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return {"status": "db error", "error": error}
    finally:
        if conn is not None:
            conn.close()
    
    return {"status": "ok", "error": None}

def road_insert_client(client_data):
    # Insert a new client into the clients table
    sql = """INSERT INTO client (img, name, description, gps) VALUES(%s, %s, %s, %s)"""
    conn = None
    client_id = None

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=secret_credentials.database["ra_db"]["HOST"],
            database=secret_credentials.database["ra_db"]["NAME"],
            user=secret_credentials.database["ra_db"]["USER"],
            password=secret_credentials.database["ra_db"]["PASSWORD"],
            port=secret_credentials.database["ra_db"]["PORT"]
        )
        
        # Create a new cursor
        cur = conn.cursor()
        
        # Execute the INSERT statement
        cur.execute(sql, (client_data['img'],client_data['name'],client_data['description'],client_data['gps'],))
        
        # Commit the changes to the database
        conn.commit()
        
        count = cur.rowcount
        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return {"status": "db error", "error": error}
    finally:
        if conn is not None:
            conn.close()
    
    return {"status": "ok", "error": None}

# Flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_image():
    # Read payload from request
    pl_str = request.get_data().decode('utf-8')
    payload = json.loads(pl_str)
    # payload = request.form.to_dict()
    name = payload["name"]
    description = payload["description"]
    gps = payload["gps"]
    request_type = payload["request_type"]
    image = payload["image"] # encoded base64 image
    image_decoded = decodestring(image.encode()) # decode image

    # Save image to directory and get abspath
    img_abspath = "{}/{}.jpg".format(CLIENT_PATH, datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")) # abspath to saved image
    img = open(img_abspath, "wb")
    img.write(image_decoded)

    # Push data to queue
    client_data = {
        "name": name,
        "description": description,
        "gps": gps,
        "img": img_abspath,
        "request_type": request_type
    }
    # Insert data to databases
    insert_status = ""
    if request_type == "ambros":
        #insert_status = rosambrosdb_insert_client(client_data) # Insert data to rosambros database for neural network
        validate = validate_single(img_abspath)
        # print debug
        timenow = datetime.datetime.now()
        dt_string = timenow.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string, "validate result:", validate)
        if validate == True:
            response = push_marker_to_map(name, description, gps, img_abspath)
            print("Response code if validate True:", response.status_code)
            return jsonify({
                "msg": "success",
                "md5": {
                    "name": hashlib.md5(name.encode("utf-8")).hexdigest(),
                    "description": hashlib.md5(description.encode("utf-8")).hexdigest(),
                    "gps": hashlib.md5(gps.encode("utf-8")).hexdigest(),
                    "image": hashlib.md5(image.encode("utf-8")).hexdigest(),
                    "request_type": hashlib.md5(image.encode("utf-8")).hexdigest(),
                }
            })
    elif request_type == "road":
        #insert_status = road_insert_client(client_data) # Insert data to complete road database
        pass

    # Return json answer
    # if insert_status["status"] != "ok":
    #     return jsonify({
    #         "msg": insert_status["status"],
    #         "error": insert_status["error"]
    #     })
    return jsonify({
        "msg": "upload error",
        "error": "upload error"
    })
    
    # return jsonify({
    #         "msg": "success",
    #         "md5": {
    #             "name": hashlib.md5(name.encode("utf-8")).hexdigest(),
    #             "description": hashlib.md5(description.encode("utf-8")).hexdigest(),
    #             "gps": hashlib.md5(gps.encode("utf-8")).hexdigest(),
    #             "image": hashlib.md5(image.encode("utf-8")).hexdigest(),
    #             "request_type": hashlib.md5(image.encode("utf-8")).hexdigest(),
    #         }
    #     })


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