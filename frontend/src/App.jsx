import React from "react";
import PromptInput from "./components/PromptInput.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import TokenStats from "./components/TokenStats.jsx";
import "./style.css";

export default function App() {
  const [messages, setMessages] = React.useState([]);
  const [stats, setStats] = React.useState({ tokens: 0, ram: "0 MB" });

  function App() {
    const [response, setResponse] = React.useState("");
    const [stats, setStats] = React.useState({ tokens: 0, ram: "0 MB" });

    return (
      <>
        <h1>EchoFrame by Alignment Stack</h1>
        <PromptInput setResponse={setMessages} setStats={setStats} />
        <TokenStats stats={stats} />
        <ChatWindow message ={response} />
      </>
    );
   }

  return (
    <div className="app">
      <h1>EchoFrame</h1>
      <h2>by Alignment Stack</h2>
      <ChatWindow messages={messages} />
      <PromptInput setResponse={setMessages} setStats={setStats} />
      <TokenStats stats={stats} />
    </div>
  );
}
