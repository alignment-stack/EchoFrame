// backend/llm-server.js

const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.post("/api/generate", async (req, res) => {
  const { prompt, model } = req.body;

  if (!prompt || !model) {
    return res.status(400).json({ error: "Prompt and model are required." });
  }

  const ollama = spawn("ollama", ["run", model], {
    stdio: ["pipe", "pipe", "inherit"],
  });

  // Stream the response back to the frontend
  res.setHeader("Content-Type", "text/plain");

  ollama.stdout.on("data", (chunk) => {
    res.write(chunk);
  });

  ollama.on("close", () => {
    res.end();
  });

  // Send the prompt to Ollama
  ollama.stdin.write(prompt + "\n");
  ollama.stdin.end();
});

app.listen(PORT, () => {
  console.log(`✅ EchoFrame backend running at http://localhost:${PORT}`);
});
