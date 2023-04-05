import os
import boto3
from io import BytesIO
from flask import Flask, request
from fastai.vision.all import *
import torchvision.transforms as T
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
model_location = os.environ['MODEL_LOCATION']
learn = None

@app.before_first_request
def initialize():
    global learn 
    learn = load_learner(model_location)

@app.route('/health-check')
def health_check():
	return "success"

@app.route('/process-image', methods=['POST'])
def process_image():
    # Get the JSON payload
    payload = request.get_json()
    # Load the file from S3 using the AWS library
    s3 = boto3.client('s3')
    path = payload['path']
    bucket = payload['bucket']

    file_byte_string = s3.get_object(Bucket=bucket, Key=path)['Body'].read()
    # Load the image and make a prediction
    bytes = BytesIO(file_byte_string).read()
    img = PILImage.create(bytes)
    img = img.convert("RGB")
    with learn.no_bar(), learn.no_logging():
        _, _, probs = learn.predict(img)
        return dict(zip(learn.dls.vocab, map(float, probs)))

if __name__ == "__main__":
    app.run(debug=True)