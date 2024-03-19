import React, { useState } from 'react';
import axios from 'axios';
import segmented_image_face from './segmented_image_face.jpg';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [segmentedImageUrl, setSegmentedImageUrl] = useState(0);
  const [file, setFile] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setFile(URL.createObjectURL(event.target.files[0]));
  };

  console.log("selectedFile", selectedFile)

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);


    try {
      const uploadResponse = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      const storedImageUrl = uploadResponse.data.storedImageUrl;
      setImageUrl(storedImageUrl);
      setSegmentedImageUrl(0);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSegmentation = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:5000/segment', { imageUrl });
      if (response.data.segmentedImageUrl) {
        setSegmentedImageUrl((prev) => prev + 1);
        setLoading(false);
      }
    } catch (error) {
      setLoading(false);
      console.error('Error:', error);
    }
  };
  console.log("setSegmentedImageUrl", segmentedImageUrl.name)

  return (
    <div className="container">
      <h1>Face Segmentation</h1>
      <div className="form-container">
        <div className='upload-container'>
          {file ? <img src={file} width="250px" height={"250px"} /> : null}
          <label htmlFor='uploadImage' className='upload-button'>
            Choose File
            <input
              type="file"
              onChange={handleFileChange}
              accept="image/*"
              style={{ display: 'none' }}
              id="uploadImage"
            />
          </label>
          <button onClick={handleUpload} className='upload-button'>Upload</button>
        </div>

      </div>
      {imageUrl && (
        <div className="form-container">
          <button onClick={handleSegmentation} className='upload-button'>Segment</button>
        </div>
      )}
      {loading ? <div>Please Wait, Segmenting the Image</div> : null}
      {segmentedImageUrl ? (
        <div className="segmented-image">
          <h2>Segmented Image</h2>
          <img src={segmented_image_face} alt="Segmented Face" width="500px" height={"300px"} />
        </div>
      ) : null}
    </div>
  );
}

export default App;
