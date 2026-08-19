import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000" });

export const getReviews = () => api.get("/reviews").then(r => r.data);

export const getReview = (id) => api.get(`/reviews/${id}`).then(r => r.data);

export const getSummary = () => api.get("/stats/summary").then(r => r.data);

export const getTimeline = () => api.get("/stats/timeline").then(r => r.data);

export const triggerReview = (repoName, prNumber) =>
     api.post(`/reviews/trigger`, null, {
          params: {
               repo_name: repoName,
               pr_number: prNumber,
          },
     });

export default api;