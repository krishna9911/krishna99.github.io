"""
Created on Mon Mar 18 20:28:21 2024

@author: krishnayadav
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import segment_image as face_segment


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'storedImageUrl': file_path}), 200

@app.route('/segment', methods=['POST'])
def segment_image():
    current_dir = os.getcwd()
    try:
        image_url = request.json.get('imageUrl')
        print("original image path:", image_url)
        output_segmented_image_path = face_segment.get_segmented_image(image_url)
        output_segmented_image_path = current_dir + '/' + output_segmented_image_path
        print("output_segmented:", output_segmented_image_path)
        if output_segmented_image_path:
            return jsonify({'segmentedImageUrl': output_segmented_image_path}), 200
        else:
            return jsonify({'error': 'Image segmentation failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
