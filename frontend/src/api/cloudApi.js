import axios from "axios";
import { auth } from "../firebase";

const BASE = "http://localhost:8000/api";

const getToken = async () => {
  const user = auth.currentUser;
  if (!user) throw new Error("User not authenticated");

  return await user.getIdToken(true); // 🔥 force refresh
};

const authHeaders = async () => {
  const token = await getToken();
  return {
    headers: { Authorization: `Bearer ${token}` }
  };
};

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

    const res = await axios.post(`${BASE}/predict/?${params}`, {}, await authHeaders());
    return res.data;
  },

  // ── PRICING TABLE ──
  pricing: async () => {
    const res = await axios.get(`${BASE}/pricing/`, await authHeaders());
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

    const res = await axios.post(`${BASE}/recommend/?${params}`, {}, await authHeaders());
    return res.data;
  },

  // ── NEW: TRENDS DATA FROM ML MODEL ──
  trends: async () => {
    const res = await axios.get(`${BASE}/trends/`, await authHeaders());
    return res.data;
  },

};

export default api;