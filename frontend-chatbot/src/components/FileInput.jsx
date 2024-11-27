import React, { useState, useRef } from 'react';
// import Button from '@mui/material/Button';
import AddCircleOutlineOutlinedIcon from '@mui/icons-material/AddCircleOutlineOutlined';
import IconButton from '@mui/material/IconButton';
import SnackBar from '@mui/material/Snackbar';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios'
import { backend_url } from '../config';

const FileInput = () => {

  const fileInputRef = useRef(null)
  const [uploadState, setUploadState] = useState("");
  const [open, setOpen] = useState(false)

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
      setUploadState(`File ${response.data.filename} was uploaded succesfully!`)
    } catch (e) {
      console.error("Error uploading file:", e);
    }
  };


  const handleFileChange = (event) => {
    setOpen(true);
    const file = event.target.files[0];
    if (file) {
      sendFileData(file);
    } else {
      console.log("No file selected.");
    }
  };

  const handleCloseSnackbar = () => {
    setOpen(false);
  }

  const action = (
    <React.Fragment>
      {/* <Button color="secondary" size="small" onClick={handleCloseSnackbar}>
        UNDO
      </Button> */}
      <IconButton
        size="small"
        aria-label="close"
        color="inherit"
        onClick={handleCloseSnackbar}
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </React.Fragment>
  );

  return (
    <div>
      <SnackBar
        open={open}
        autoHideDuration={6500}
        onClose={handleCloseSnackbar}
        message={uploadState}
        action={action}
      />
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
