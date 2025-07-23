export default function ChatWindow ( { messages }) {
  return (
    <div className="chat-window">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.role}`}>
          <strong>{message.role === "user" ? "You" : "Assistant"}:</strong>
          <p>{message.content}</p>
        </div>
      ))}
    </div>
  );
}
// This component renders the chat messages in a scrollable window.
// It maps over the messages array and displays each message with its role (user or assistant).
// The messages are styled differently based on their role for better readability.
// The `key` prop is used to uniquely identify each message in the list, which helps React optimize rendering