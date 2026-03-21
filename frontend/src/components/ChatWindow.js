import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const SUGGESTIONS = [
  "What is the total revenue?",
  "What are the main risk factors?",
  "Summarize key highlights",
  "What is the net profit margin?",
  "What is the future outlook?",
];

function ChatWindow({ docProcessed }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendQuestion = async (q) => {
    const userQuestion = q || question;
    if (!userQuestion.trim()) return;

    // Add user message
    setMessages(prev => [...prev, {
      type: 'user',
      text: userQuestion
    }]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/ask`, {
        question: userQuestion
      });

      // Add bot message
      setMessages(prev => [...prev, {
        type: 'bot',
        text: response.data.answer
      }]);

    } catch (err) {
      setMessages(prev => [...prev, {
        type: 'bot',
        text: '❌ Error: ' + (err.response?.data?.detail || 'Something went wrong!')
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendQuestion();
    }
  };

  const clearChat = () => setMessages([]);

  // Welcome Screen
  if (!docProcessed) {
    return (
      <div className="welcome">
        <div className="welcome-icon">💰</div>
        <div className="welcome-title">AI Financial Assistant</div>
        <div className="welcome-sub">
          Upload your financial documents and get instant AI-powered insights
        </div>
        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">📄</div>
            <div className="feature-title">Smart PDF Analysis</div>
            <div className="feature-desc">
              Extract insights from annual reports and statements
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <div className="feature-title">Natural Language Q&A</div>
            <div className="feature-desc">
              Ask questions in plain English
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <div className="feature-title">Powered by RAG</div>
            <div className="feature-desc">
              Accurate answers from your documents
            </div>
          </div>
        </div>
        <div style={{
          marginTop: '32px',
          color: '#444',
          fontSize: '13px'
        }}>
          ← Upload a PDF from the sidebar to get started
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>

      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px'
      }}>
        <div>
          <div className="page-title">💬 Document Q&A</div>
          <div className="page-sub">Ask anything about your document</div>
        </div>
        {messages.length > 0 && (
          <button
            className="btn btn-danger"
            style={{ width: 'auto', padding: '6px 16px' }}
            onClick={clearChat}
          >
            🗑️ Clear
          </button>
        )}
      </div>

      {/* Suggestions */}
      {messages.length === 0 && (
        <div className="suggestions">
          {SUGGESTIONS.map((s, i) => (
            <button
              key={i}
              className="suggestion-btn"
              onClick={() => sendQuestion(s)}
              disabled={loading}
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', marginBottom: '16px' }}>
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={
                msg.type === 'user'
                  ? 'chat-bubble-user'
                  : 'chat-bubble-bot'
              }
            >
              {msg.type === 'user' ? '❓ ' : '💬 '}
              {msg.text}
            </div>
          ))}

          {/* Loading bubble */}
          {loading && (
            <div className="chat-bubble-bot">
              <div className="loading">
                <div className="spinner"></div>
                Analyzing document...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <input
          className="chat-input"
          type="text"
          placeholder="Ask a question about your document..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button
          className="chat-send-btn"
          onClick={() => sendQuestion()}
          disabled={loading || !question.trim()}
        >
          🚀
        </button>
      </div>

    </div>
  );
}

export default ChatWindow;