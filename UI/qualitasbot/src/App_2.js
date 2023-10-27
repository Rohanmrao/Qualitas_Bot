import React, { useState } from "react";
import "./styles.css"

function App_2() {
  const [messages, setMessages] = useState([
    { text: "Hello I'm QualitasBot, how can I assist you?", sender: "bot" },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false); 

  const printChatBubble = () => {
    if (input.trim() !== "") {
      setLoading(true);

      // Making a GET request to the Flask endpoint with the user's input as a query parameter
      fetch(`http://192.168.1.178:5000/?user_input=${encodeURIComponent(input)}`)
        .then(response => response.text())
        .then(data => {
          setMessages([...messages, { text: input, sender: "user" }, { text: data, sender: "bot" }]);
          console.log(messages); // logging the updated messages state
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        })
        .finally(() => {
       
          setLoading(false); // loading status is set to false after the message fetch
        });
      setInput("");
    }
  };

  return (
    <div className="App">
      <div className="container mt-3">
        {messages.map((message, index) => (
          <div key={index} className={`row ${message.sender === "user" ? "justify-content-end" : ""}`}>
            <div className="col-6 text-right">
              <div className={`p-3 mb-2 ${message.sender === "user" ? "bg-secondary" : "bg-info"} text-${message.sender === "user" ? "white" : "dark"} rounded`}>
                {message.text}
              </div>
            </div>
          </div>
        ))}
      </div>
        <div className="input-container footer">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter') {
                e.preventDefault();
                printChatBubble();
              }
            }}
            placeholder="Type a message..."
          />
          
          {/* <button onClick={printChatBubble} className="button">Send Message</button> */}
        </div>
      {loading && <div className="loading-animation spinner center-screen"></div>} 
    </div>
  );
}

export default App_2;
