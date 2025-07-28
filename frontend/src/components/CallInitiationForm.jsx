// frontend/src/components/CallInitiationForm.jsx
import React, { useState } from 'react';
import { originateCall } from '../services/callApi';
import Button from './common/Button';
import Input from './common/Input';

const CallInitiationForm = () => {
  const [toNumber, setToNumber] = useState('');
  const [status, setStatus] = useState({ message: '', type: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!toNumber) {
      setStatus({ message: 'Please enter a phone number.', type: 'error' });
      return;
    }
    setLoading(true);
    setStatus({ message: '', type: '' });

    try {
      // For now, we'll hardcode agent_id=1. You could make this a dropdown later.
      const response = await originateCall(toNumber, 1);
      setStatus({ message: `Successfully initiated call! SID: ${response.data.call_sid}`, type: 'success' });
      setToNumber('');
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setStatus({ message: `Call initiation failed: ${errorMessage}`, type: 'error' });
      console.error("Call initiation failed:", error.response || error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Start a New Call</h2>
      <form onSubmit={handleSubmit}>
        <Input
          label="Phone Number to Call"
          name="toNumber"
          value={toNumber}
          onChange={(e) => setToNumber(e.target.value)}
          placeholder="+15551234567"
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
  );
};

export default CallInitiationForm;