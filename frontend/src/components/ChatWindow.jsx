import React from "react";

export default function ChatWindow({ messages }) {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`message ${msg.role === "user" ? "user" : "assistant"}`}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
}
