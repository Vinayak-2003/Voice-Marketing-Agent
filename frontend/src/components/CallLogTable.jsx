// frontend/src/components/CallLogTable.jsx
import React from 'react';

const CallLogTable = () => {
  // This would typically fetch data from a store or API
  const logs = [
    { id: 1, sid: 'CA123...', from: '+15551234567', startTime: '2023-10-27 10:00 AM', status: 'Completed' },
    { id: 2, sid: 'CA456...', from: '+15557654321', startTime: '2023-10-27 10:05 AM', status: 'In Progress' },
  ];

  return (
    <div className="card">
      <h2>Recent Calls</h2>
      <p>Call log functionality is not yet implemented in the backend.</p>
      {/* 
      // This is what the table would look like when data is available
      <table>
        <thead>
          <tr>
            <th>Call SID</th>
            <th>From</th>
            <th>Start Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td>{log.sid}</td>
              <td>{log.from}</td>
              <td>{log.startTime}</td>
              <td>{log.status}</td>
            </tr>
          ))}
        </tbody>
      </table> 
      */}
    </div>
  );
};

export default CallLogTable;