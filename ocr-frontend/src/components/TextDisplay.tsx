import Card from '@mui/material/Card';

interface TextDisplayProps {
    texts: string[];
}

export default function TextDisplay({ texts }: TextDisplayProps) {
    return (
        <div>
            <h2>OCR Texts</h2>
            {texts.length > 0 ? texts.map((text, index) => (
                <Card key={index}>
                    {text}
                </Card>
            )) : <p>No texts found</p>}
        </div>
    )
}