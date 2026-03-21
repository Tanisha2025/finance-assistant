import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function CompareDoc() {
  const [company1, setCompany1] = useState('');
  const [company2, setCompany2] = useState('');
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCompare = async () => {
    if (!file1 || !file2 || !company1 || !company2 || !question) {
      setError('Please fill all fields and upload both PDFs!');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file1', file1);
      formData.append('file2', file2);
      formData.append('company1', company1);
      formData.append('company2', company2);
      formData.append('question', question);

      const response = await axios.post(
        `${API_URL}/compare`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      setResult(response.data.result);

    } catch (err) {
      setError(
        err.response?.data?.detail || 'Comparison failed!'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="page-title">⚖️ Compare Documents</div>
      <div className="page-sub">
        Upload two financial PDFs and compare them side by side
      </div>

      {/* Upload Grid */}
      <div className="compare-grid">

        {/* Document 1 */}
        <div className="compare-card compare-card-1">
          <div className="compare-card-title">📄 Document 1</div>

          <div className="input-group">
            <div className="input-label">COMPANY NAME</div>
            <input
              className="text-input"
              placeholder="e.g. Tesla"
              value={company1}
              onChange={(e) => setCompany1(e.target.value)}
            />
          </div>

          <div className="input-group">
            <div className="input-label">UPLOAD PDF</div>
            <label className="upload-area">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile1(e.target.files[0])}
              />
              <div className="upload-icon">📄</div>
              <div className="upload-text">
                {file1 ? file1.name : 'Click to upload PDF'}
              </div>
            </label>
          </div>
        </div>

        {/* Document 2 */}
        <div className="compare-card compare-card-2">
          <div className="compare-card-title">📄 Document 2</div>

          <div className="input-group">
            <div className="input-label">COMPANY NAME</div>
            <input
              className="text-input"
              placeholder="e.g. Apple"
              value={company2}
              onChange={(e) => setCompany2(e.target.value)}
            />
          </div>

          <div className="input-group">
            <div className="input-label">UPLOAD PDF</div>
            <label className="upload-area">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile2(e.target.files[0])}
              />
              <div className="upload-icon">📄</div>
              <div className="upload-text">
                {file2 ? file2.name : 'Click to upload PDF'}
              </div>
            </label>
          </div>
        </div>

      </div>

      {/* Question Input */}
      <div className="input-group">
        <div className="input-label">COMPARISON QUESTION</div>
        <input
          className="text-input"
          placeholder="e.g. Compare the revenue and profit margins"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
      </div>

      {/* Error */}
      {error && <div className="error-msg">{error}</div>}

      {/* Compare Button */}
      <button
        className="btn btn-primary"
        onClick={handleCompare}
        disabled={loading}
        style={{ marginBottom: '24px' }}
      >
        {loading
          ? '⏳ Analyzing both documents...'
          : '⚖️ Compare Now!'
        }
      </button>

      {/* Loading */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          This may take 1-2 minutes — analyzing both documents!
        </div>
      )}

      {/* Results */}
      {result && (
        <div>
          <hr className="divider" />
          <div className="page-title" style={{ fontSize: '18px' }}>
            📊 Comparison Results
          </div>

          {/* Side by side answers */}
          <div className="compare-grid" style={{ marginTop: '16px' }}>
            <div className="compare-card compare-card-1">
              <div className="compare-card-title">
                📄 {result.doc1_name}
              </div>
              <div style={{
                color: '#ccc',
                fontSize: '13px',
                lineHeight: '1.7'
              }}>
                {result.doc1_answer}
              </div>
            </div>

            <div className="compare-card compare-card-2">
              <div className="compare-card-title">
                📄 {result.doc2_name}
              </div>
              <div style={{
                color: '#ccc',
                fontSize: '13px',
                lineHeight: '1.7'
              }}>
                {result.doc2_answer}
              </div>
            </div>
          </div>

          {/* Final Comparison */}
          <div style={{ marginTop: '8px' }}>
            <div className="page-title" style={{ fontSize: '16px' }}>
              🏆 Final Verdict
            </div>
            <div className="result-box" style={{ marginTop: '12px' }}>
              {result.comparison}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default CompareDoc;