import React from "react";
import "../style.css";

export default function App() {
  const [messages, setMessages] = React.useState([]);
  const [stats, setStats] = React.useState({ tokens: 0, ram: "0 MB" });

  return (
    <div className="app-container">
      <h1>EchoFrame UI</h1>
    </div>
  );
}
