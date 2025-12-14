import React, { useEffect, useState } from 'react';
import { adminAPI, auditAPI } from '../services/api';

interface AuditLog {
  id: number;
  actor_id: number;
  action: string;
  target: string;
  timestamp: string;
}

const AdminPanel = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [newCourse, setNewCourse] = useState({ code: '', title: '', capacity: 30 });
  const [message, setMessage] = useState('');

  // VULNERABLE: This runs for ANY user who visits this page, 
  // proving that the backend doesn't check roles for the audit API.
  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const data = await auditAPI.getLogs();
      setLogs(data);
    } catch (err) {
      console.error("Failed to fetch logs - though in this version, it likely won't fail!");
    }
  };

  const handleCreateCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await adminAPI.createCourse(newCourse);
      setMessage("Success: Course created using the Trust Boundary (Secret Header)!");
      fetchLogs(); // Refresh logs to show the new action
    } catch (err) {
      setMessage("Error: Course creation failed.");
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Registrar & Administrative Console</h1>
      <hr />

      <section style={{ marginBottom: '40px' }}>
        <h2>Create New Course</h2>
        <form onSubmit={handleCreateCourse} style={{ display: 'flex', gap: '10px', flexDirection: 'column', width: '300px' }}>
          <input placeholder="Course Code (e.g. CS101)" onChange={e => setNewCourse({...newCourse, code: e.target.value})} />
          <input placeholder="Course Title" onChange={e => setNewCourse({...newCourse, title: e.target.value})} />
          <input type="number" placeholder="Capacity" onChange={e => setNewCourse({...newCourse, capacity: Number(e.target.value)})} />
          <button type="submit" style={{ background: 'green', color: 'white', padding: '10px' }}>Create Course</button>
        </form>
        {message && <p style={{ color: 'blue' }}>{message}</p>}
      </section>

      <section>
        <h2>System Audit Logs (Sensitive Information)</h2>
        <p style={{ color: 'red' }}>Warning: These logs are visible to any logged-in student (Broken Access Control).</p>
        <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#eee' }}>
              <th>ID</th>
              <th>Timestamp</th>
              <th>User ID</th>
              <th>Action</th>
              <th>Target</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
                <td>{log.actor_id}</td>
                <td>{log.action}</td>
                <td>{log.target}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default AdminPanel;