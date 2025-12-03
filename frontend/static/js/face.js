// face.js
// Handles face registration for students and live face attendance for faculty

/**
 * Student: Register/Update Face (face_register.html)
 * Handle photo upload OR webcam capture, call /face/register.
 */
document.getElementById('registerFaceBtn')?.addEventListener('click', async function() {
  // TODO: Capture image from webcam/file; POST to /face/register
  document.getElementById('faceRegisterAlert').style.display = 'block';
  document.getElementById('faceRegisterAlert').innerText = 'Face registration not implemented yet.';
});

// Webcam capture logic for students
// TODO: Implement webcam streaming and capture (optional)

/**
 * Faculty: Start/Stop Live Face Attendance (face_attendance.html)
 * Calls /face/recognize every 300ms with latest webcam frame
 * Updates recognizedStudentsTable in real-time
 */
document.getElementById('startFaceAttendance')?.addEventListener('click', function() {
  // TODO: Start webcam, begin polling /face/recognize
  alert('Live face attendance start not implemented yet.');
});
document.getElementById('stopFaceAttendance')?.addEventListener('click', function() {
  // TODO: Stop webcam/recognition polling
  alert('Live face attendance stop not implemented yet.');
});
