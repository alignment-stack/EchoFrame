import React, { useState } from "react";

export default function PromptInput({ setResponse, setStats }) {
  const [prompt, setPrompt] = useState("");
  const [model, setModel] = useState("llama2"); // Default model

  const handleKeyDown = async (e) => {
    if (e.key === "Enter") {
      e.preventDefault();

      if (!prompt.trim()) return;

      const userMessage = { role: "user", content: prompt };
      setResponse((prev) => [...prev, userMessage]);
      setPrompt(""); // Clear input field

      try {
        const res = await fetch("http://localhost:3001/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt, model }),
        });

        if (!res.ok || !res.body) {
          setResponse((prev) => [
            ...prev,
            { role: "assistant", content: fullResponse },
          ]);
          return;
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = "";
        let tokens = 0;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value);
          fullResponse += chunk;
          tokens += chunk.split(/\s+/).length;

          setStats({
            tokens,
            ram: `${(performance.memory?.usedJSHeapSize / 1048576 || 0).toFixed(1)} MB`,
          });

          // Update the assistant's message as it streams
          setResponse((prev) => {
            // Replace the last assistant message if it exists, otherwise add a new one
            const last = prev[prev.length - 1];
            if (last && last.role === "assistant") {
              return [
                ...prev.slice(0, -1),
                { role: "assistant", content: fullResponse },
              ];
            } else {
              return [
                ...prev,
                { role: "assistant", content: fullResponse },
              ];
            }
          });
        }
      } catch (error) {
        setResponse((prev) => [
          ...prev,
          { role: "error", content: "Error: Failed to fetch" },
        ]);
      }
    }
  };

  return (
    <div style={{ marginBottom: "1em", textAlign: "center" }}>
      <select
        value={model}
        onChange={(e) => setModel(e.target.value)}
        style={{
          padding: "0.5em",
          fontSize: "1em",
          marginBottom: "1em",
          borderRadius: "4px",
          border: "1px solid #ccc",
          backgroundColor: "#1e1e1e",
          color: "#eee",
        }}
      >
        <option value="llama2">LLaMA 2</option>
        <option value="mistral">Mistral</option>
        <option value="gemma">Gemma</option>
      </select>

      <textarea
        placeholder="Type your prompt and hit Enter..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={3}
        style={{
          width: "80%",
          padding: "1em",
          fontSize: "1em",
          backgroundColor: "#1e1e1e",
          color: "#fff",
          border: "1px solid #333",
          borderRadius: "6px",
          resize: "none",
        }}
      />
    </div>
  );
}
