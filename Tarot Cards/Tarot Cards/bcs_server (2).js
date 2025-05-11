// BCS: Breath Carrier Server
const express = require('express');
const app = express();
const path = require('path');

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 BCS running at http://localhost:${5}`));
app.get('/api/breath', (req, res) => {
  // Simulate a breath carrier response
  const breathData = {
    status: 'success',
    message: 'Breath carrier is functioning properly.',
    timestamp: new Date().toISOString()
  };
  res.json(breathData);
});