import React, { useRef } from 'react';
import AddCircleOutlineOutlinedIcon from '@mui/icons-material/AddCircleOutlineOutlined';
import IconButton from '@mui/material/IconButton';
import axios from 'axios'
import { backend_url } from '../config';

const FileInput = () => {

  const fileInputRef = useRef(null)

  const handleButtonClick = () => {
    fileInputRef.current.click();
  }

  //Send file data to the API
  const sendFileData = async (file) => {
    try {
      const formData = new FormData();
      formData.append("file", file);  // Make sure "file" matches the backend's expected field name

      const response = await axios.post(`${backend_url}/file`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",  // Make sure the header is set for file upload
        },
      });

      console.log("File uploaded successfully:", response.data);
    } catch (e) {
      console.error("Error uploading file:", e);
    }
  };


  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      sendFileData(file);
    } else {
      console.log("No file selected.");
    }
  };


  return (
    <div>

      <label htmlFor="fileInput">
        <IconButton color="primary" onClick={handleButtonClick}>
          <AddCircleOutlineOutlinedIcon sx={{ fill: '#a6a6a7', fontSize: 22 }} />
        </IconButton>
      </label>
      <input
        type="file"
        ref={fileInputRef}
        id="fileInput"
        onChange={handleFileChange}
        className='upload_file'
      />


    </div>
  );
};

export default FileInput;
