import React, { useState } from "react";
import "./styles.css"

function App() {
  const [messages, setMessages] = useState([
    { text: "Hello I'm QualitasBot, how can I assist you?", sender: "bot" },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false); 

  const printChatBubble = () => {
    if (input.trim() !== "") {
      setLoading(true);

      // Making a GET request to the Flask endpoint with the user's input as a query parameter
      {/* The overall strcuture for the fetch request is defined by three primary variables or status flags, which is directly operated by Javascript's UseState hook
        
          i) messages -> Describes the text and it's subsequent details - 
            a) text : can either be 'input' from the user or 'data' from the bot
            b) sender : can either be 'bot' or 'user'

          ii) loading -> Boolean flag to mark whether the code is in loading stage or not 
            a) SetLoading : True/False, triggers when the loading screen pops up 
          
          iii) input -> Uses the 'input' tag in HTML to take in user input.
            a) setInput : Initially set to empty string at the time of fetch, to reset the user's input and make room for a new question
          
        */}


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

  {/* Note to self - MDN docs on handling a basic aynschronous promise- 

            function async_function() {
          return new Promise((resolve, reject) => {
            if (<some condition>)) {
              resolve('Success');
            } else {
              reject(new Error('Failed'));
            }
          });
        }

        checkvalue()
          .then((variable) => {
            console.log(variable); // print the resolved variable's value
          })
          .catch((err) => {
            console.error(err); // print the rejected variable's value, an error in this case
          })
          .finally(() => {
            console.log('Experiment completed');  // print this once the promise has yielded something, either a resolve or a reject
          });
*/}

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

export default App;
