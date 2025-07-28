// frontend/src/pages/DashboardPage.jsx
import React, { useState } from 'react';
import { originateCall } from '../services/callApi'; // We will create this service next
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import CallLogTable from '../components/CallLogTable';

const DashboardPage = () => {
  const [toNumber, setToNumber] = useState('');
  const [agentId, setAgentId] = useState('1'); // Default to agent ID 1
  const [status, setStatus] = useState({ message: '', type: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!toNumber || !agentId) {
      setStatus({ message: 'Phone number and agent ID are required.', type: 'error' });
      return;
    }
    setLoading(true);
    setStatus({ message: '', type: '' });

    try {
      // CRITICAL FIX: Ensure agentId is sent as an integer.
      const response = await originateCall(toNumber, parseInt(agentId));
      setStatus({ message: `Success! Call SID: ${response.data.call_sid}`, type: 'success' });
      setToNumber('');
    } catch (error) {
      // CRITICAL FIX: Correctly display the detailed error message.
      const errorMessage = error.response?.data?.detail || error.message || 'An unknown error occurred.';
      setStatus({ message: `Error: ${errorMessage}`, type: 'error' });
      console.error("Call initiation failed:", error.response || error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>
      
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2>Start a New Call</h2>
        <form onSubmit={handleSubmit}>
          <Input
            label="Phone Number to Call (e.g., +15551234567)"
            name="toNumber"
            value={toNumber}
            onChange={(e) => setToNumber(e.target.value)}
            required
          />
          <Input
            label="Agent ID"
            name="agentId"
            value={agentId}
            onChange={(e) => setAgentId(e.target.value)}
            type="number"
            required
          />
          <Button type="submit" disabled={loading}>
            {loading ? 'Calling...' : 'Start Call'}
          </Button>
        </form>
        {status.message && (
          <p style={{ color: status.type === 'error' ? 'red' : 'green', marginTop: '1rem' }}>
            {status.message}
          </p>
        )}
      </div>

      <p>Monitor call activity below.</p>
      <div style={{ marginTop: '2rem' }}>
        <CallLogTable />
      </div>
    </div>
  );
};

export default DashboardPage;