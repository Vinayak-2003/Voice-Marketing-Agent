// frontend/src/pages/AgentDetailPage.jsx
import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import useAgentStore from '../store/agentStore';

const AgentDetailPage = () => {
  const { agentId } = useParams();
  const { currentAgent, fetchAgentById, loading, error } = useAgentStore();

  useEffect(() => {
    fetchAgentById(agentId);
  }, [agentId, fetchAgentById]);

  if (loading) return <p>Loading agent details...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;
  if (!currentAgent) return <p>Agent not found.</p>;

  return (
    <div>
      <div className="page-header">
        <h1>Agent: {currentAgent.name}</h1>
        <Link to="/agents">Back to Agents</Link>
      </div>
      <div className="card">
        <h3>Details</h3>
        <p><strong>ID:</strong> {currentAgent.id}</p>
        <p><strong>Voice ID:</strong> {currentAgent.voice_id}</p>
        <h3>System Prompt</h3>
        <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f0f0f0', padding: '1rem', borderRadius: '6px' }}>
          {currentAgent.system_prompt}
        </pre>
      </div>
    </div>
  );
};

export default AgentDetailPage;