// frontend/src/components/CampaignList.jsx
import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you'll have a detail page later

const CampaignList = ({ campaigns }) => {
  if (campaigns.length === 0) {
    return <div className="card"><p>No campaigns found. Click "+ New Campaign" to get started!</p></div>;
  }

  return (
    <div className="card">
      <table className="campaign-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Agent ID</th>
            <th>Status</th>
            <th>Contacts</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {campaigns.map(campaign => (
            <tr key={campaign.id}>
              <td>{campaign.name}</td>
              <td>{campaign.agent_id}</td>
              <td>
                <span className={`status-badge status-${campaign.status.toLowerCase()}`}>
                  {campaign.status}
                </span>
              </td>
              <td>{campaign.contacts.length}</td>
              <td>
                {/* Placeholder for future campaign detail page */}
                <Link to={`/campaigns/${campaign.id}`} className="action-link">View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CampaignList;