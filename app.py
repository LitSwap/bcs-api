from flask import Flask, request
import cv2
import tensorflow as tf
import numpy as np
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'litswap-project-33d210b26f63.json'
raw_dir =  "bookImages/raw"
processed_dir = "bookImages/processed"
model_path = "model/2406122239_300_model_4points"
bucket_name = "books-litswap"


model = tf.keras.models.load_model(model_path)

def download_cs_file(bucket_name, file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True

def upload_cs_file(bucket_name, source_file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)

    return True



def process_image(image_path):
    image = cv2.imread(image_path)
    H, W, _ = image.shape # get image width and height
    S = 300 # S is input image size

    input_image = cv2.resize(image, (S, S))
    input_image = np.expand_dims(input_image, axis=0)

    # Predict the edges using the model
    prediction = model.predict(input_image)[0]

    # adjust the prediction
    prediction = prediction * np.array([W/S, H/S])

    # rows adjustment
    prediction[[2,3]] = prediction[[3,2]]
    prediction = prediction.astype(np.float32())

    final_points = np.array([[0,0], [500,0], [0,600], [500,600]], np.float32)

    transform_mat = cv2.getPerspectiveTransform(prediction, final_points)

    result = cv2.warpPerspective(image, transform_mat, (500, 600))
    
    # Save the processed image
    cv2.imwrite(image_path, result)

    processed_img_path = os.path.join(processed_dir, image_path)

    upload_cs_file(bucket_name, image_path, processed_img_path)

    os.remove(image_path)
    
    return os.path.join("https://storage.googleapis.com/", bucket_name, processed_img_path).replace(" ", "%20")

# Initializing flask application
app = Flask(__name__)

@app.route("/")
def main():
    return """
        Application is working
    """

# Process images
@app.route("/process", methods=["POST"])
def processReq():
    filename = request.form["filename"]
    raw_img_path = os.path.join(raw_dir, filename)
    download_cs_file(bucket_name, raw_img_path, filename)

    resp = process_image(filename)

    return resp

if __name__ == "__main__":
    app.run(debug=False,port=int(os.environ.get("PORT", 8080)),host="0.0.0.0")
