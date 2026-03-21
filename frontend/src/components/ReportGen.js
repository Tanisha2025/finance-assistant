import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function ReportGen({ docProcessed, docStats }) {
  const [companyName, setCompanyName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleGenerateReport = async () => {
    if (!companyName.trim()) {
      setError('Please enter company name!');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post(
        `${API_URL}/generate-report`,
        { company_name: companyName },
        { responseType: 'blob' }
      );

      // PDF download karo
      const blob = new Blob(
        [response.data],
        { type: 'application/pdf' }
      );
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${companyName}_Financial_Report.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);

      setSuccess('✅ Report generated and downloaded!');

    } catch (err) {
      setError('Report generation failed! Try again.');
    } finally {
      setLoading(false);
    }
  };

  // Not processed screen
  if (!docProcessed) {
    return (
      <div className="welcome">
        <div className="welcome-icon">📊</div>
        <div className="welcome-title">Auto Report Generator</div>
        <div className="welcome-sub">
          Please upload and process a document first!
        </div>
        <div style={{
          color: '#444',
          fontSize: '13px'
        }}>
          ← Upload a PDF from the sidebar
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="page-title">📊 Auto Report Generator</div>
      <div className="page-sub">
        Generate a professional PDF report from your document
      </div>

      {/* Document Info */}
      <div style={{
        background: '#1a1a2e',
        border: '1px solid #2e2e4e',
        borderRadius: '10px',
        padding: '16px',
        marginBottom: '24px',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <div style={{ fontSize: '24px' }}>📄</div>
        <div>
          <div style={{ color: '#fff', fontWeight: '600' }}>
            {docStats.filename}
          </div>
          <div style={{ color: '#555', fontSize: '12px' }}>
            {docStats.pages} pages · {docStats.chunks} chunks indexed
          </div>
        </div>
        <div className="status-ready" style={{ marginLeft: 'auto' }}>
          ● Ready
        </div>
      </div>

      {/* What report includes */}
      <div style={{
        background: '#1a1a2e',
        border: '1px solid #2e2e4e',
        borderRadius: '10px',
        padding: '20px',
        marginBottom: '24px'
      }}>
        <div style={{
          color: '#00f5d4',
          fontSize: '13px',
          fontWeight: '600',
          marginBottom: '12px'
        }}>
          📋 Report will include:
        </div>

        {[
          '📌 Executive Summary',
          '💰 Key Financial Metrics',
          '⚠️ Risk Factors Analysis',
          '🌟 Key Highlights',
          '🔮 Future Outlook & Guidance',
        ].map((item, i) => (
          <div key={i} style={{
            color: '#666',
            fontSize: '13px',
            padding: '6px 0',
            borderBottom: i < 4 ? '1px solid #1e1e2e' : 'none'
          }}>
            {item}
          </div>
        ))}
      </div>

      {/* Company Name Input */}
      <div className="input-group">
        <div className="input-label">COMPANY NAME</div>
        <input
          className="text-input"
          placeholder="e.g. Tesla, Apple, Paytm"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
        />
      </div>

      {/* Error / Success */}
      {error && <div className="error-msg">{error}</div>}
      {success && <div className="success-msg">{success}</div>}

      {/* Generate Button */}
      <button
        className="btn btn-primary"
        onClick={handleGenerateReport}
        disabled={loading || !companyName.trim()}
      >
        {loading
          ? '⏳ Generating Report... (30-60 sec)'
          : '📄 Generate PDF Report'
        }
      </button>

      {/* Loading */}
      {loading && (
        <div className="loading" style={{ marginTop: '16px' }}>
          <div className="spinner"></div>
          <div>
            <div>AI is analyzing your document...</div>
            <div style={{ color: '#444', fontSize: '11px', marginTop: '4px' }}>
              Generating 5 sections — please wait!
            </div>
          </div>
        </div>
      )}

      {/* Tips */}
      <div style={{
        marginTop: '32px',
        padding: '16px 20px',
        background: 'rgba(0,245,212,0.05)',
        border: '1px solid rgba(0,245,212,0.15)',
        borderRadius: '10px',
      }}>
        <div style={{
          color: '#00f5d4',
          fontSize: '12px',
          fontWeight: '600',
          marginBottom: '8px'
        }}>
          🎯 Pro Tip
        </div>
        <div style={{ color: '#555', fontSize: '12px', lineHeight: '1.7' }}>
          For best results, upload official annual reports or 
          10-K filings. The AI will extract key financial metrics,
          risks, and insights automatically!
        </div>
      </div>

    </div>
  );
}

export default ReportGen;