import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://35.154.86.118:8000";

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

  // Instructor decision (UPDATED)
  makeDecision: (reviewId, decision, notes = null, autoMerge = false) => {
    return api.post(`/api/reviews/${reviewId}/decide`, {
      decision,
      notes,
      auto_merge: autoMerge, // ← NEW
    });
  },

  // Get statistics
  getStats: () => {
    return api.get("/api/reviews/stats/summary");
  },

  // NEW: Check PR merge status
  getPRStatus: (reviewId) => {
    return api.get(`/api/reviews/${reviewId}/pr-status`);
  },
};

export default api;

// import axios from "axios";

// // const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
// const API_BASE_URL = import.meta.env.VITE_API_URL || "http://65.0.107.153:8000";

// const api = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// export const reviewsAPI = {
//   // Get all reviews
//   getAllReviews: (status = null) => {
//     const params = status ? { status } : {};
//     return api.get("/api/reviews", { params });
//   },

//   // Get single review
//   getReview: (reviewId) => {
//     return api.get(`/api/reviews/${reviewId}`);
//   },

//   // Instructor decision
//   makeDecision: (reviewId, decision, notes = null) => {
//     return api.post(`/api/reviews/${reviewId}/decide`, {
//       decision,
//       notes,
//     });
//   },

//   // Get statistics
//   getStats: () => {
//     return api.get("/api/reviews/stats/summary");
//   },
// };

// export default api;
