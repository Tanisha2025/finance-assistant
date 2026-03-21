import React, { useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import CompareDoc from './components/CompareDoc';
import ReportGen from './components/ReportGen';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [docProcessed, setDocProcessed] = useState(false);
  const [docStats, setDocStats] = useState({
    filename: '',
    pages: 0,
    chunks: 0
  });

  return (
    <div className="app">
      {/* Sidebar */}
      <Sidebar
        docProcessed={docProcessed}
        setDocProcessed={setDocProcessed}
        docStats={docStats}
        setDocStats={setDocStats}
      />

      {/* Main Content */}
      <div className="main">

        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Single Document Q&A
          </button>
          <button
            className={`tab ${activeTab === 'compare' ? 'active' : ''}`}
            onClick={() => setActiveTab('compare')}
          >
            ⚖️ Compare Documents
          </button>
          <button
            className={`tab ${activeTab === 'report' ? 'active' : ''}`}
            onClick={() => setActiveTab('report')}
          >
            📊 Auto Report
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'chat' && (
            <ChatWindow docProcessed={docProcessed} />
          )}
          {activeTab === 'compare' && (
            <CompareDoc />
          )}
          {activeTab === 'report' && (
            <ReportGen docProcessed={docProcessed} docStats={docStats} />
          )}
        </div>

      </div>
    </div>
  );
}

export default App;