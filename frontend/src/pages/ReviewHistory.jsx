import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getReviews, triggerReview } from "../api";

export default function ReviewHistory() {
     const [reviews, setReviews] = useState([]);
     const [loading, setLoading] = useState(true);
     const [error, setError] = useState(null);

     // Modal & Form State
     const [isModalOpen, setIsModalOpen] = useState(false);
     const [repoName, setRepoName] = useState("");
     const [prNumber, setPrNumber] = useState("");
     const [triggering, setTriggering] = useState(false);
     const [triggerMessage, setTriggerMessage] = useState("");

     const navigate = useNavigate();

     const loadReviews = () => {
          setLoading(true);
          getReviews()
               .then(setReviews)
               .catch(() => setError("Failed to load reviews."))
               .finally(() => setLoading(false));
     };

     useEffect(() => {
          loadReviews();
     }, []);

     const handleTrigger = async () => {
          setTriggerMessage("");
          setError(null);

          if (!repoName || !prNumber) {
               setTriggerMessage("Enter repository name and PR number.");
               return;
          }

          setTriggering(true);

          try {
               await triggerReview(repoName, prNumber);
               setTriggerMessage("Review triggered successfully.");
               setRepoName("");
               setPrNumber("");
               loadReviews();
               // Close modal after brief delay on success
               setTimeout(() => setIsModalOpen(false), 1500);
          } catch {
               setTriggerMessage("Failed to trigger review.");
          } finally {
               setTriggering(false);
          }
     };

     const openModal = () => {
          setTriggerMessage("");
          setIsModalOpen(true);
     };

     if (loading) {
          return (
               <div className="state-container">
                    <div className="state-title">Loading reviews...</div>
               </div>
          );
     }

     if (error) {
          return (
               <div className="state-container error-container">
                    <div className="state-title">Unable to load reviews</div>
                    <div className="state-desc">{error}</div>
                    <button className="btn btn-secondary" onClick={loadReviews}>Retry</button>
               </div>
          );
     }

     // Derived Metrics
     const totalReviews = reviews.length;
     const completedReviews = reviews.filter(r => r.status === "completed").length;
     const totalFindings = reviews.reduce((sum, r) => sum + (r.total_findings || 0), 0);

     return (
          <div>
               <div className="page-header">
                    <div>
                         <h2 className="page-title">Review History</h2>
                         <div className="page-subtitle">Monitor and inspect automated pull request reviews.</div>
                    </div>
                    <button className="btn btn-primary" onClick={openModal}>
                         + Trigger Review
                    </button>
               </div>

               {/* Metrics */}
               <div className="metrics-grid">
                    <div className="metric-card">
                         <div className="metric-label">Total Reviews</div>
                         <div className="metric-value">{totalReviews}</div>
                    </div>
                    <div className="metric-card">
                         <div className="metric-label">Completed</div>
                         <div className="metric-value">{completedReviews}</div>
                    </div>
                    <div className="metric-card">
                         <div className="metric-label">Total Findings</div>
                         <div className="metric-value">{totalFindings}</div>
                    </div>
               </div>

               {/* Empty State vs Table */}
               {reviews.length === 0 ? (
                    <div className="state-container">
                         <div style={{ fontSize: '48px', marginBottom: '16px', opacity: 0.8 }}>🔍</div>
                         <div className="state-title">No reviews yet</div>
                         <div className="state-desc">Trigger your first AI-powered code review to see results here.</div>
                         <button className="btn btn-primary" onClick={openModal}>
                              + Trigger Review
                         </button>
                    </div>
               ) : (
                    <div className="table-container">
                         <table className="data-table">
                              <thead>
                                   <tr>
                                        <th>Repository</th>
                                        <th>PR</th>
                                        <th>Status</th>
                                        <th>Findings</th>
                                        <th>Created</th>
                                   </tr>
                              </thead>
                              <tbody>
                                   {reviews.map((r) => (
                                        <tr
                                             key={r.id}
                                             onClick={() => navigate(`/reviews/${r.id}`)}
                                             className="clickable"
                                        >
                                             <td className="td-repo">{r.repo_name}</td>
                                             <td className="td-pr">#{r.pr_number}</td>
                                             <td>
                                                  <span className={`badge ${r.status}`}>{r.status}</span>
                                             </td>
                                             <td className="td-mono">{r.total_findings !== null ? r.total_findings : "—"}</td>
                                             <td className="td-mono" style={{ color: "var(--text-secondary)" }}>
                                                  {new Date(r.created_at).toLocaleString(undefined, {
                                                       month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                                                  })}
                                             </td>
                                        </tr>
                                   ))}
                              </tbody>
                         </table>
                    </div>
               )}

               {/* Trigger Review Modal */}
               {isModalOpen && (
                    <div className="modal-overlay" onClick={() => setIsModalOpen(false)}>
                         <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                              <div className="modal-header">
                                   <div>
                                        <div className="modal-title">Trigger New Review</div>
                                        <div className="modal-subtitle">Start an AI-powered analysis of a pull request</div>
                                   </div>
                                   <button className="modal-close" onClick={() => setIsModalOpen(false)}>✕</button>
                              </div>
                              
                              <div className="modal-body">
                                   <div className="form-group">
                                        <label className="form-label">Repository Name</label>
                                        <input
                                             type="text"
                                             className="form-input"
                                             placeholder="user/repository"
                                             value={repoName}
                                             onChange={(e) => setRepoName(e.target.value)}
                                        />
                                   </div>

                                   <div className="form-group">
                                        <label className="form-label">Pull Request Number</label>
                                        <input
                                             type="number"
                                             className="form-input"
                                             placeholder="42"
                                             value={prNumber}
                                             onChange={(e) => setPrNumber(e.target.value)}
                                        />
                                   </div>

                                   {triggerMessage && (
                                        <div style={{ marginTop: '12px', fontSize: '13px', color: triggerMessage.includes('Failed') || triggerMessage.includes('Enter') ? 'var(--danger)' : 'var(--success)' }}>
                                             {triggerMessage}
                                        </div>
                                   )}
                              </div>

                              <div className="modal-footer">
                                   <button 
                                        className="btn btn-secondary" 
                                        onClick={() => setIsModalOpen(false)}
                                        disabled={triggering}
                                   >
                                        Cancel
                                   </button>
                                   <button 
                                        className="btn btn-primary" 
                                        onClick={handleTrigger}
                                        disabled={triggering}
                                   >
                                        {triggering ? "Triggering..." : "Trigger Review"}
                                   </button>
                              </div>
                         </div>
                    </div>
               )}
          </div>
     );
}
