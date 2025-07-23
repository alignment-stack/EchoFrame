import React from "react";
import ReactDOM from "react-dom/client";
import PromptInput from "./PromptInput.jsx";
import ChatWindow from "./ChatWindow.jsx";
import TokenStats from "./TokenStats.jsx";
import "./style.css";

function App() {
  const [response, setResponse] = React.useState("");
  const [stats, setStats] = React.useState({ tokens: 0, ram: "0 MB" });

  return (
    <>
      <h1>EchoFrame by Alignment Stack</h1>
      <PromptInput setResponse={setResponse} setStats={setStats} />
      <TokenStats stats={stats} />
      <ChatWindow response={response} />
      <h2> by Alignment Stack</h2>
    </>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);


