import axios from "axios";

// const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://65.0.107.153:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const reviewsAPI = {
  // Get all reviews
  getAllReviews: (status = null) => {
    const params = status ? { status } : {};
    return api.get("/api/reviews", { params });
  },

  // Get single review
  getReview: (reviewId) => {
    return api.get(`/api/reviews/${reviewId}`);
  },

  // Instructor decision
  makeDecision: (reviewId, decision, notes = null) => {
    return api.post(`/api/reviews/${reviewId}/decide`, {
      decision,
      notes,
    });
  },

  // Get statistics
  getStats: () => {
    return api.get("/api/reviews/stats/summary");
  },
};

export default api;
