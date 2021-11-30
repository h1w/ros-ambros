import os
from flask import Flask, jsonify, request, redirect, url_for
from PIL import Image
import hashlib
import psycopg2
import datetime
from pathlib import Path
from base64 import decodestring

# Constants
CLIENT_PATH = "/var/www/html/rosambros/clients/images"
REPOSITORY_DIR = Path(__file__).resolve().parent.parent

# Import credentials module contains secret data
from importlib.machinery import SourceFileLoader
secret_credentials = SourceFileLoader('module.secret_credentials', '{}/secret_credentials.py'.format(REPOSITORY_DIR)).load_module()


# Postgresql section
def insert_client(client_data):
    # Insert a new client into the clients table
    sql = """INSERT INTO client (img, name, description, gps) VALUES(%s, %s, %s, %s)"""
    conn = None
    client_id = None

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=secret_credentials.database["rosambros"]["HOST"],
            database=secret_credentials.database["rosambros"]["NAME"],
            user=secret_credentials.database["rosambros"]["USER"],
            password=secret_credentials.database["rosambros"]["PASSWORD"],
            port=secret_credentials.database["rosambros"]["PORT"]
        )
        
        # Create a new cursor
        cur = conn.cursor()
        
        # Execute the INSERT statement
        cur.execute(sql, (client_data['img'],client_data['name'],client_data['description'],client_data['gps'],))
        
        # Get the generated id back
        #client_id = cur.fetchone()[0]
        
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
    payload = request.form.to_dict()
    name = payload["name"]
    description = payload["description"]
    gps = payload["gps"]
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
        "img": img_abspath
    }
    insert_status = insert_client(client_data) # Insert data to database
    
    # Return json answer
    if insert_status["status"] != "ok":
        return jsonify({
            "msg": insert_status["status"],
            "error": insert_status["error"]
        })
    
    return jsonify({
            "msg": "success",
            "md5": {
                "name": hashlib.md5(name.encode("utf-8")).hexdigest(),
                "description": hashlib.md5(description.encode("utf-8")).hexdigest(),
                "gps": hashlib.md5(gps.encode("utf-8")).hexdigest(),
                "image": hashlib.md5(image.encode("utf-8")).hexdigest()
            }
        })


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