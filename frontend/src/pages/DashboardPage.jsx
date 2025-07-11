// frontend/src/pages/DashboardPage.jsx
import React from 'react';
import CallLogTable from '../components/CallLogTable';

const DashboardPage = () => {
  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>
      <p>Welcome to the VoiceGenie dashboard. Here you can monitor call activity and manage your AI agents.</p>
      <div style={{ marginTop: '2rem' }}>
        <CallLogTable />
      </div>
    </div>
  );
};

export default DashboardPage;