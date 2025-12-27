import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  try {
    const imagesDirectory = path.join(process.cwd(), 'public', 'butterfly-images');

    // Check if directory exists
    if (!fs.existsSync(imagesDirectory)) {
      return res.status(200).json({ images: [] });
    }

    // Read all files from the directory
    const files = fs.readdirSync(imagesDirectory);

    // Filter for image files only
    const imageFiles = files.filter(file => {
      const ext = path.extname(file).toLowerCase();
      return ['.jpg', '.jpeg', '.png', '.gif', '.webp'].includes(ext);
    });

    res.status(200).json({ images: imageFiles });
  } catch (error) {
    console.error('Error reading images directory:', error);
    res.status(500).json({ error: 'Failed to read images', images: [] });
  }
}
