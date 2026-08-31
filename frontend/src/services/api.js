import axios from 'axios';

const rawApiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const BASE_URL = rawApiUrl.endsWith('/api') ? rawApiUrl : `${rawApiUrl.replace(/\/$/, '')}/api`;

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export const loginUser = async (username, password) => {
  const res = await apiClient.post('/auth/login', { username, password });
  return res.data;
};

export const fetchHealth = async () => {
  const res = await apiClient.get('/health');
  return res.data;
};

export const fetchDashboardSummary = async () => {
  const res = await apiClient.get('/dashboard');
  return res.data;
};

export const fetchAnimalsList = async (params = {}) => {
  const res = await apiClient.get('/animals', { params });
  return res.data;
};

export const registerCow = async (payload) => {
  const res = await apiClient.post('/animals/register', payload);
  return res.data;
};

export const fetchAnimalDetail = async (animalId) => {
  const res = await apiClient.get(`/animals/${animalId}`);
  return res.data;
};

export const fetchSensorData = async (animalId) => {
  const res = await apiClient.get(`/sensor-data/${animalId}`);
  return res.data;
};

export const runPredict = async (payload) => {
  const res = await apiClient.post('/predict', payload);
  return res.data;
};

export const fetchModelPerformance = async () => {
  const res = await apiClient.get('/model-performance');
  return res.data;
};
