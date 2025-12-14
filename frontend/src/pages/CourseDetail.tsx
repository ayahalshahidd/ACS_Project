import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { coursesAPI, enrollmentsAPI } from '../services/api';

const CourseDetail = () => {
  // useParams returns strings, but our API expects a number
  const { id } = useParams<{ id: string }>();
  const [course, setCourse] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Get user from localStorage (VULNERABLE: Easy to manipulate)
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    if (id) {
      // FIX 1: Convert string ID to number using Number() or parseInt()
      coursesAPI.getById(Number(id))
        .then((data) => {
          setCourse(data);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [id]);

  const handleEnroll = async () => {
    // VULNERABLE: CSRF 
    // This sends a POST request with cookies but no CSRF token.
    if (course && user.id) {
      try {
        await enrollmentsAPI.create(course.id, user.id);
        alert("Enrollment successful!");
      } catch (err) {
        alert("Enrollment failed.");
      }
    }
  };

  // FIX 2: Guard clause to prevent "course is possibly null" errors
  if (loading) return <div>Loading course details...</div>;
  if (!course) return <div>Course not found.</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h1>{course.title}</h1>
      <p>Code: {course.code}</p>
      <p>Description: {course.description}</p>
      <p>Capacity: {course.capacity}</p>
      
      <button 
        onClick={handleEnroll} 
        style={{ padding: '10px 20px', background: 'blue', color: 'white', cursor: 'pointer' }}
      >
        Enroll in this Course
      </button>
    </div>
  );
};

export default CourseDetail;