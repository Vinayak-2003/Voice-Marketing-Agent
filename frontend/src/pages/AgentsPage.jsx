// frontend/src/pages/AgentsPage.jsx

import React, { useEffect, useState } from 'react';
import AgentForm from '../components/AgentForm';
import useAgentStore from '../store/agentStore';
import { Link } from 'react-router-dom';
// --- IMPORT THE NEW API FUNCTION ---
import { originateCall } from '../services/agentApi';

// A new component for the call functionality
const AgentActions = ({ agent }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [callStatus, setCallStatus] = useState('');

  const handleCall = async () => {
    if (!phoneNumber) {
      alert('Please enter a phone number in E.164 format (e.g., +15551234567).');
      return;
    }
    setCallStatus('Initiating call...');
    try {
      // --- USE THE CENTRALIZED API FUNCTION ---
      const response = await originateCall(agent.id, phoneNumber);
      setCallStatus(response.data.message || 'Call initiated successfully!');
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to initiate call.';
      setCallStatus(`Error: ${errorMessage}`);
      console.error('Call initiation failed:', error);
    }
  };

  return (
    <div style={{ marginTop: '10px', borderTop: '1px solid #eee', paddingTop: '10px', display: 'flex', alignItems: 'center', gap: '10px' }}>
      <input
        type="text"
        className="input"
        placeholder="Enter phone number to call"
        value={phoneNumber}
        onChange={(e) => setPhoneNumber(e.target.value)}
        style={{ flexGrow: 1 }}
      />
      <button onClick={handleCall} className="button">Call with this Agent</button>
      {callStatus && <p style={{ fontSize: '0.8em', margin: 0, whiteSpace: 'nowrap' }}>{callStatus}</p>}
    </div>
  );
};


const AgentsPage = () => {
  const { agents, loading, error, fetchAgents } = useAgentStore();

  useEffect(() => {
    fetchAgents();
  }, [fetchAgents]);

  return (
    <div>
      <div className="page-header">
        <h1>Voice Agents</h1>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        <div>
          <div className="card">
            <h2>Existing Agents</h2>
            {loading && <p>Loading agents...</p>}
            {error && <p style={{ color: 'red' }}>Error: {error}</p>}
            
            {/* --- ADDED A SAFETY CHECK HERE --- */}
            {/* This prevents the app from crashing if 'agents' is not yet an array */}
            {!loading && !error && agents && (
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {agents.map((agent) => (
                  <li key={agent.id} style={{ marginBottom: '1rem', borderBottom: '1px solid #f0f0f0', paddingBottom: '1rem' }}>
                    <Link to={`/agents/${agent.id}`} style={{ fontSize: '1.2rem', fontWeight: 'bold', textDecoration: 'none', color: 'var(--primary-color)' }}>
                      {agent.name}
                    </Link>
                    <AgentActions agent={agent} />
                  </li>
                ))}
              </ul>
            )}
            {!loading && agents.length === 0 && <p>No agents created yet.</p>}
          </div>
        </div>
        <div>
          <AgentForm onFormSubmit={fetchAgents} />
        </div>
      </div>
    </div>
  );
};

export default AgentsPage;