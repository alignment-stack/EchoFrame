import React, { useState } from "react";

export default function PromptInput({ setMessages, setStats }) {
  const [prompt, setPrompt] = useState("");
  const [model, setModel] = useState("llama2");

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setMessages(prev => [...prev, { role: "user", content: prompt }]);
    setPrompt("");

    try {
      const res = await fetch("http://localhost:3001/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, model })
      });

      if (!res.ok || !res.body) {
        setMessages(prev => [...prev, { role: "error", content: "Server returned no response." }]);
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
          ram: `${(performance.memory?.usedJSHeapSize / 1048576 || 0).toFixed(1)} MB`
        });
      }

      setMessages(prev => [...prev, { role: "assistant", content: fullResponse.trim() }]);

    } catch (err) {
      setMessages(prev => [...prev, { role: "error", content: "Error: " + err.message }]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="prompt-input">
      <select value={model} onChange={e => setModel(e.target.value)}>
        <option value="llama2">LLaMA 2</option>
        <option value="mistral">Mistral</option>
        <option value="phi">Phi</option>
        {/* Add more options if desired */}
      </select>
      <textarea
        placeholder="Type your prompt and hit Enter..."
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={2}
      />
      <button onClick={handleSubmit}>Send</button>
    </div>
  );
}
