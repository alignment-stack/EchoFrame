import React from "react";
import PromptInput from "./components/PromptInput.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import TokenStats from "./components/TokenStats.jsx";
import "./style.css";

export default function App() {
  const [messages, setMessages] = React.useState([]);
  const [stats, setStats] = React.useState({ tokens: 0, ram: "0 MB" });

  return (
    <div className="app">
      <h1>EchoFrame</h1>
      <h2>by Alignment Stack</h2>
      <ChatWindow messages={messages} />
      <PromptInput setMessages={setMessages} setStats={setStats} />
      <TokenStats stats={stats} />
    </div>
  );
}
