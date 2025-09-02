import axios from "axios";

// Base Axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",  // Django API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Add JWT token automatically (if available)
api.interceptors.request.use((config) => {
  // Do NOT add Authorization header for login or register
  if (
    config.url.includes("auth/login") ||
    config.url.includes("auth/register")
  ) {
    return config;
  }
  const token = localStorage.getItem("access"); // Use "access" instead of "access_token"
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default {
  login(data) {
    return api.post("auth/login/", data);
  },
  register(data) {
    return api.post("auth/register/", data);
  },
  getUser() {
    return api.get("auth/get_user/");
  },
  getWarehouses() { // <-- Add this method
    return api.get("warehouses/");
  },
  deleteWarehouse(uuid) {
    return api.delete(`warehouses/${uuid}/`);
  },
  getInchargeUsers() {
    return api.get('auth/get_user/');
  },
  addWarehouse(data) {
    return api.post("warehouses/", data);
  },
  updateWarehouse(uuid, data) {
    return api.put(`warehouses/${uuid}/`, data);
  },
  getVendors() {
    return api.get("vendors/");
  },
  addVendor(data) {
    return api.post("vendors/", data);
  },
  updateVendor(uuid, data) {
    return api.put(`vendors/${uuid}/`, data);
  },
  deleteVendor(uuid) {
    return api.delete(`vendors/${uuid}/`);
  },
};
