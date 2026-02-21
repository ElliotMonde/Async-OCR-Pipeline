import { useEffect, useState } from 'react'
import './App.css'
import UploadBox from './components/UploadBox'
import TextDisplay from './components/TextDisplay'
import TextInput from './components/TextInput'
import { Box, Paper, Typography, Container, Stack } from '@mui/material'

interface UploadResponse {
  task_id: string;
}

interface SyncUploadResponse {
  text: string | string[];
}

interface GetTextsResponse {
  task_id: string[];
}

function App() {
  const [texts, setTexts] = useState<string[]>([])
  const [syncTexts, setSyncTexts] = useState<string[]>([])
  const [taskIds, setTaskIds] = useState<string[]>([])
  const [images, setImages] = useState<File[]>([])
  const [asyncUploaded, setAsyncUploaded] = useState<boolean>(false)
  const [syncUploaded, setSyncUploaded] = useState<boolean>(false)
  const [uploadedAlert, setUploadedAlert] = useState<string>("")
  function convert_to_base64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = error => reject(error);
    });
  }

  async function upload_images(images: File[]) {
    try {
      const base64Strings = await Promise.all(
        images.map((image) => convert_to_base64(image))
      );

      const res: Response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/image`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image_data: base64Strings,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server validation error:", errorData);
        return;
      }

      const data: UploadResponse = await res.json();
      setTaskIds([...taskIds, data.task_id]);
      setUploadedAlert("Images uploaded successfully.");
    } catch (error) {
      console.error("Upload failed:", error);
    }
  }

  async function sync_upload_images(images: File[]) {
    try {
      const base64Strings = await Promise.all(
        images.map((image) => convert_to_base64(image))
      );

      const res: Response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/image-sync`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image_data: base64Strings,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server validation error:", errorData);
        return;
      }

      const data: SyncUploadResponse = await res.json();
      setSyncTexts(Array.isArray(data.text) ? data.text : [data.text]);
      setUploadedAlert("Images uploaded successfully.");
    } catch (error) {
      console.error("Upload failed:", error);
    }
  }

  async function get_texts(task_id: string) {
    const res: Response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/image/?task_id=${task_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data: GetTextsResponse = await res.json();
    console.log("data", data)
    setTexts(data.task_id);
  }

  useEffect(() => {
    if (images.length > 0 && asyncUploaded) {
      upload_images(images);
      setAsyncUploaded(false);
    }
  }, [asyncUploaded]);

  useEffect(() => {
    if (images.length > 0 && syncUploaded) {
      sync_upload_images(images);
      setSyncUploaded(false);
    }
  }, [syncUploaded]);

  return (
    <Container maxWidth={false} sx={{ py: 4, height: '100vh' }}>
      <Stack direction={{ xs: 'column', md: 'row' }} spacing={4} sx={{ height: '100%' }}>

        <Box sx={{ flex: 1, width: '100%' }}>
          <Paper elevation={3} sx={{ p: 4, height: '100%', display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Typography variant="h4" component="h1" align="center" gutterBottom>
              Sync OCR
            </Typography>

            <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <UploadBox setImages={setImages} setUploadBool={setSyncUploaded} />

              {uploadedAlert && syncUploaded && (
                <Typography color="success.main" align="center">{uploadedAlert}</Typography>
              )}

              <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
                <TextDisplay texts={syncTexts} />
              </Box>
            </Box>
          </Paper>
        </Box>

        <Box sx={{ flex: 1, width: '100%' }}>
          <Paper elevation={3} sx={{ p: 4, height: '100%', display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Typography variant="h4" component="h1" align="center" gutterBottom>
              Async OCR
            </Typography>

            <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <UploadBox setImages={setImages} setUploadBool={setAsyncUploaded} />

              {uploadedAlert && asyncUploaded && (
                <Typography color="success.main" align="center">{uploadedAlert}</Typography>
              )}

              <Box>
                <Typography variant="h6" gutterBottom>Task IDs</Typography>
                <TextDisplay texts={taskIds} />
              </Box>

              <Box sx={{ my: 2 }}>
                <TextInput onClick={get_texts} />
              </Box>

              <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
                <Typography variant="h6" gutterBottom>Results</Typography>
                <TextDisplay texts={texts} />
              </Box>
            </Box>
          </Paper>
        </Box>

      </Stack>
    </Container>
  )
}

export default App
