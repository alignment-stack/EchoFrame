import React from "react";

export default function TokenStats({ stats }) {
  return (
    <div className="token-stats">
      <div>Tokens: {stats.tokens}</div>
      <div>RAM: {stats.ram}</div>
    </div>
  );
}
