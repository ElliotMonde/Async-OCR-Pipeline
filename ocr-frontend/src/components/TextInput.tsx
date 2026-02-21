import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { useState } from 'react'


interface TextInputProps {
    onClick: CallableFunction;
}
export default function TextInput({ onClick }: TextInputProps) {
    const [taskId, setTaskId] = useState<string>("");
    return (
        <>
        <h2>Get OCR texts from Task ID</h2>
        <TextField label="Task ID" variant="outlined" value={taskId} onChange={(e) => setTaskId(e.target.value)}></TextField>
        <Button variant="contained" onClick={() => onClick(taskId)}>Submit</Button>
        </>
    )
}