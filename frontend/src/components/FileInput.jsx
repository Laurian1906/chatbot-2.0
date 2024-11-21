import React, { useState } from 'react';

const FileInput = () => {

  return (
    <div className='container'>
      <label>Upload file
        <input
          type="file"
          onChange={handleFileChange}
          className='upload_file'
        />
      </label>

    </div>
  );
};

export default FileInput;
