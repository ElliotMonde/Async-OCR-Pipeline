import { useRef, useState } from 'react';
import { Box, Typography } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';

interface UploadBoxProps {
    setImages: (images: File[]) => void;
    setUploadBool: CallableFunction;
}

export default function MultiImageUpload({setImages, setUploadBool}: UploadBoxProps) {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

    const handleBoxClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(event.target.files || []);
        setSelectedFiles(files);
        setImages(files);
        setUploadBool(true);
    };

    return (
        <>
            <h2>Upload Images</h2>
            <Box
                onClick={handleBoxClick}
                sx={{
                    border: '2px dashed #ccc',
                    borderRadius: 2,
                    padding: 4,
                    textAlign: 'center',
                    cursor: 'pointer',
                    '&:hover': { borderColor: 'primary.main' },
                }}
            >
                <UploadFileIcon fontSize="large" color="primary" />
                <Typography>Click to upload multiple images</Typography>

                <input
                    type="file"
                    multiple
                    hidden
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    accept="image/*"
                />
            </Box>
            <Box mt={2}>
                {selectedFiles.map((file) => (
                    <Typography key={file.name}>{file.name}</Typography>
                ))}
            </Box>
        </>
    );
}
