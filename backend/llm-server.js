const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(bodyParser.json());
app.use(express.json());

app.post('/api/generate', (req, res) => {
  const { prompt, model } = req.body;

  if (!prompt || !model) {
    return res.status(400).send('Missing prompt or model');
  }

  console.log(`[+] Received prompt for model "${model}": ${prompt}`);

  const ollama = spawn('ollama', ['run', model], {
    stdio: ['pipe', 'pipe', 'inherit']
  });

  // Send prompt to Ollama
  ollama.stdin.write(prompt + '\n');
  ollama.stdin.end();

  res.setHeader('Content-Type', 'text/plain');

  ollama.stdout.on('data', chunk => {
    res.write(chunk);
  });

  ollama.stdout.on('end', () => {
    res.end();
    console.log(`[✓] Completed request for model "${model}"`);
  });

  ollama.on('error', err => {
    console.error('[!] Error spawning Ollama:', err);
    res.status(500).send('Internal server error');
  });
});

app.listen(PORT, () => {
  console.log(`🧠 EchoFrame backend running at http://localhost:${PORT}`);
});