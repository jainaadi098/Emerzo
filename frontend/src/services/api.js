import axios from 'axios';

// Backend Address
// const API_URL = 'https://emerzo-backend.onrender.com/';
const API_URL = 'https://emerzo-backend.onrender.com';

// 1. Patient SOS Trigger
export const triggerEmergency = async (latitude, longitude) => {
  try {
    const response = await axios.post(`${API_URL}/api/emergency`, {
      latitude,
      longitude
    });
    return response.data;
  } catch (error) {
    console.error("SOS Error:", error);
    throw error;
  }
};

// 2. Hospital Polling (Fetch Requests)
export const fetchHospitalRequests = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/hospital/requests`);
    return response.data;
  } catch (error) {
    console.error("Polling Error:", error);
    return []; // Error aane par empty list bhejo
  }
};

// 3. Hospital Accept Request
export const acceptRequest = async (requestId) => {
  try {
    const response = await axios.post(`${API_URL}/api/hospital/accept/${requestId}`);
    return response.data;
  } catch (error) {
    console.error("Accept Error:", error);
    throw error;
  }
};