// ─── API SERVICE LAYER ────────────────────────────────────────────────────────
// When your backend is ready, swap the mock functions with real axios calls.
// Step 1: npm install axios
// Step 2: uncomment the import below
// import axios from "axios";

const BASE = "http://localhost:8000/api";

const api = {
  predict: async ({ vcpu, ram_gb, storage_gb, usage_hours }) => {
    // ─── MOCK (delete this block when backend is ready) ───
    await new Promise(r => setTimeout(r, 1200));
    const base = vcpu * 8 + ram_gb * 3.5 + storage_gb * 0.08 + (usage_hours / 720) * 12;
    return {
      predicted_monthly_cost_usd: parseFloat(base.toFixed(2)),
      providers: {
        AWS:   parseFloat((base * 1.05).toFixed(2)),
        Azure: parseFloat((base * 1.02).toFixed(2)),
        GCP:   parseFloat((base * 0.96).toFixed(2)),
      },
      recommendation: base * 0.96 < base * 1.02 ? "GCP" : "Azure",
      savings_vs_most_expensive: parseFloat((base * 1.05 - base * 0.96).toFixed(2)),
    };
    // ─── REAL (uncomment when backend is ready) ───────────
    // const params = new URLSearchParams({ vcpu, ram_gb, storage_gb, usage_hours }).toString();
    // const res = await axios.post(`${BASE}/predict/?${params}`);
    // return res.data;
  },

  pricing: async () => {
    // ─── MOCK (delete this block when backend is ready) ───
    await new Promise(r => setTimeout(r, 600));
    return [
      { provider: "AWS",   instance: "t3.micro",      vcpu: 2, ram: 1,  price: 0.0104 },
      { provider: "AWS",   instance: "t3.medium",     vcpu: 2, ram: 4,  price: 0.0416 },
      { provider: "AWS",   instance: "m5.large",      vcpu: 2, ram: 8,  price: 0.0960 },
      { provider: "Azure", instance: "B2s",           vcpu: 2, ram: 4,  price: 0.0416 },
      { provider: "Azure", instance: "D2s_v3",        vcpu: 2, ram: 8,  price: 0.0960 },
      { provider: "GCP",   instance: "e2-medium",     vcpu: 2, ram: 4,  price: 0.0335 },
      { provider: "GCP",   instance: "n2-standard-2", vcpu: 2, ram: 8,  price: 0.0971 },
    ];
    // ─── REAL (uncomment when backend is ready) ───────────
    // const res = await axios.get(`${BASE}/pricing`);
    // return res.data;
  },
};

export default api;