import React, { useEffect, useState } from 'react';
import { enrollmentsAPI, coursesAPI } from '../services/api';

interface Enrollment {
  id: number;
  course_id: number;
  status: string;
  timestamp: string;
}

const Dashboard = () => {
  const [enrollments, setEnrollments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // VULNERABLE: IDOR (Insecure Direct Object Reference)
  // We are pulling the user ID from localStorage. 
  // An attacker can change "id": 2 to "id": 1 in their browser to see someone else's dashboard.
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    if (user.id) {
      fetchData();
    }
  }, [user.id]);

  const fetchData = async () => {
    try {
      // Step 1: Get all enrollments for this user ID
      const enrollmentData = await enrollmentsAPI.getByUser(user.id);
      
      // Step 2: For each enrollment, fetch the actual course details to show the title
      const enrichedData = await Promise.all(
        enrollmentData.map(async (en: Enrollment) => {
          const course = await coursesAPI.getById(en.course_id);
          return { ...en, courseTitle: course.title, courseCode: course.code };
        })
      );
      
      setEnrollments(enrichedData);
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch dashboard data");
      setLoading(false);
    }
  };

  const handleDrop = async (enrollmentId: number) => {
    // VULNERABLE: IDOR in DELETE
    // We don't verify if the enrollment belongs to the user on the frontend or backend.
    if (window.confirm("Are you sure you want to drop this course?")) {
      await enrollmentsAPI.delete(enrollmentId);
      fetchData(); // Refresh
    }
  };

  if (loading) return <div>Loading your schedule...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h1>Welcome, {user.email}</h1>
      <p>Role: <strong>{user.role}</strong></p>
      
      <section style={{ marginTop: '30px' }}>
        <h2>Your Current Registrations</h2>
        {enrollments.length === 0 ? (
          <p>You are not enrolled in any courses yet.</p>
        ) : (
          <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
            <thead>
              <tr style={{ background: '#f0f0f0' }}>
                <th>Course Code</th>
                <th>Course Title</th>
                <th>Status</th>
                <th>Enrolled On</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {enrollments.map((en) => (
                <tr key={en.id}>
                  <td>{en.courseCode}</td>
                  <td>{en.courseTitle}</td>
                  <td>
                    <span style={{ 
                      color: en.status === 'enrolled' ? 'green' : 'red',
                      fontWeight: 'bold' 
                    }}>
                      {en.status.toUpperCase()}
                    </span>
                  </td>
                  <td>{new Date(en.timestamp).toLocaleDateString()}</td>
                  <td>
                    {en.status === 'enrolled' && (
                      <button 
                        onClick={() => handleDrop(en.id)}
                        style={{ background: 'red', color: 'white', border: 'none', padding: '5px 10px', cursor: 'pointer' }}
                      >
                        Drop
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section style={{ marginTop: '40px', padding: '20px', background: '#fffbe6', border: '1px solid #ffe58f' }}>
        <h3>Timetable & Holds</h3>
        <p>No active holds on your account.</p>
        <p><em>Timetable visualization stub: Monday 10:00 AM - 12:00 PM (Room 302)</em></p>
      </section>
    </div>
  );
};

export default Dashboard;