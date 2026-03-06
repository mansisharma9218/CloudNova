import axios from "axios";

const BASE = "http://localhost:8000/api";

const getToken = () => localStorage.getItem("token");

const authHeaders = () => ({
  headers: { Authorization: `Bearer ${getToken()}` }
});

const api = {

  // ── COST PREDICTION ──
  predict: async ({ vcpu, ram_gb, storage_gb, usage_hours, region, pricing_model }) => {
    const params = new URLSearchParams({
      vcpu,
      ram_gb,
      storage_gb,
      usage_hours,
      region,
      pricing_model
    }).toString();

    const res = await axios.post(`${BASE}/predict/?${params}`, {}, authHeaders());
    return res.data;
  },

  // ── PRICING TABLE ──
  pricing: async () => {
    const res = await axios.get(`${BASE}/pricing/`, authHeaders());
    return res.data;
  },

  // ── RECOMMENDATION ENGINE ──
  recommend: async ({ vcpu, ram_gb, storage_gb, usage_hours, budget }) => {
    const params = new URLSearchParams({
      vcpu,
      ram_gb,
      storage_gb,
      usage_hours,
      ...(budget && { budget })
    }).toString();

    const res = await axios.post(`${BASE}/recommend/?${params}`, {}, authHeaders());
    return res.data;
  },

  // ── NEW: TRENDS DATA FROM ML MODEL ──
  trends: async () => {
    const res = await axios.get(`${BASE}/trends/`, authHeaders());
    return res.data;
  },

};

export default api;