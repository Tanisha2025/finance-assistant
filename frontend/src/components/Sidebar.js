import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function Sidebar({ docProcessed, setDocProcessed, docStats, setDocStats }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setError('');
    setSuccess('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file!');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post(
        `${API_URL}/upload`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      setDocProcessed(true);
      setDocStats(response.data.stats);
      setSuccess('✅ Document processed successfully!');

    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sidebar">

      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">💰</div>
        <div className="sidebar-logo-title">FinanceAI</div>
        <div className="sidebar-logo-sub">Powered by LLaMA + RAG</div>
      </div>

      {/* Upload Section */}
      <div className="sidebar-label">UPLOAD DOCUMENT</div>

      <label className="upload-area">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
        />
        <div className="upload-icon">📄</div>
        <div className="upload-text">
          Click to upload PDF
        </div>
      </label>

      {/* Selected File */}
      {selectedFile && (
        <div className="upload-filename">
          📄 {selectedFile.name}
          <div style={{ color: '#555', fontSize: '10px', marginTop: '4px' }}>
            {(selectedFile.size / 1024).toFixed(1)} KB
          </div>
        </div>
      )}

      {/* Messages */}
      {error && <div className="error-msg">{error}</div>}
      {success && <div className="success-msg">{success}</div>}

      {/* Process Button */}
      <button
        className="btn btn-primary"
        onClick={handleUpload}
        disabled={loading || !selectedFile}
      >
        {loading ? '⏳ Processing...' : '⚡ Process Document'}
      </button>

      {/* Stats */}
      {docProcessed && (
        <>
          <hr className="divider" />
          <div className="sidebar-label">DOCUMENT STATS</div>
          <div className="stat-grid">
            <div className="stat-card">
              <div className="stat-number">{docStats.pages}</div>
              <div className="stat-label">Pages</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{docStats.chunks}</div>
              <div className="stat-label">Chunks</div>
            </div>
          </div>
          <div style={{
            background: 'rgba(0,245,212,0.05)',
            border: '1px solid #00f5d433',
            borderRadius: '8px',
            padding: '10px',
            fontSize: '11px',
            color: '#555',
            wordBreak: 'break-all'
          }}>
            📄 {docStats.filename}
          </div>
        </>
      )}

      {/* Tech Stack */}
      <div className="tech-stack">
        <div className="tech-stack-title">TECH STACK</div>
        <div className="tech-item">🧠 LLaMA 3.3 70B</div>
        <div className="tech-item">🔗 LangChain</div>
        <div className="tech-item">🗄️ ChromaDB</div>
        <div className="tech-item">⚡ FastAPI</div>
        <div className="tech-item">⚛️ React</div>
      </div>

    </div>
  );
}

export default Sidebar;