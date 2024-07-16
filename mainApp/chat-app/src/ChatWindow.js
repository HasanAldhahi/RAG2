import React, { useState, useEffect, useRef } from 'react';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = () => {
    if (inputMessage.trim() !== '') {
      setMessages([...messages, { text: inputMessage, isUser: true }]);
      sendMessageToServer(inputMessage);
      setInputMessage('');
    }
  };

  const sendMessageToServer = (message) => {
    // Simulating server response
    setTimeout(() => {
      setMessages(prevMessages => [...prevMessages, { text: `Server received: ${message}`, isUser: false }]);
    }, 1000);
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div id="chat-container" className="max-w-[500px] mx-auto">
            <div 
              ref={chatBoxRef} 
              className="max-h-[600px] overflow-y-auto border border-gray-300 rounded-lg p-4 mb-4"
            >
              {messages.map((msg, index) => (
                <div key={index} className={`mb-2 p-2 rounded-lg ${msg.isUser ? 'bg-blue-100 text-blue-800' : 'bg-gray-200 text-gray-800'}`}>
                  {msg.text}
                </div>
              ))}
            </div>
            <div className="flex">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                className="flex-grow rounded-l-lg border border-gray-300 p-2"
                placeholder="Type your message..."
              />
              <button 
                onClick={sendMessage}
                className="bg-blue-500 text-white rounded-r-lg px-4 py-2"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
