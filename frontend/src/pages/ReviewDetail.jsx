import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getReview } from "../api";

export default function ReviewDetail() {
     const { id } = useParams();
     const navigate = useNavigate();

     const [review, setReview] = useState(null);
     const [loading, setLoading] = useState(true);
     const [error, setError] = useState(null);

     useEffect(() => {
          getReview(id)
               .then(setReview)
               .catch(() => setError("Failed to load review."))
               .finally(() => setLoading(false));
     }, [id]);

     if (loading) {
          return (
               <div className="state-container">
                    <div className="state-title">Loading review...</div>
               </div>
          );
     }

     if (error) {
          return (
               <div className="state-container error-container">
                    <div className="state-title">Unable to load review</div>
                    <div className="state-desc">{error}</div>
                    <button className="btn btn-secondary" onClick={() => window.location.reload()}>Retry</button>
               </div>
          );
     }

     if (!review) {
          return (
               <div className="state-container">
                    <div className="state-title">Review not found</div>
                    <div className="state-desc">The requested code review does not exist.</div>
                    <button className="btn btn-primary" onClick={() => navigate('/')}>Return Home</button>
               </div>
          );
     }

     const findings = review.findings || [];
     
     // Severity Metrics
     const highFindings = findings.filter(f => f.severity === "high" || f.severity === "HIGH").length;
     const mediumFindings = findings.filter(f => f.severity === "medium" || f.severity === "MEDIUM").length;
     const lowFindings = findings.filter(f => f.severity === "low" || f.severity === "LOW").length;

     return (
          <div>
               <button className="btn btn-back" onClick={() => navigate('/')}>
                    ← Back to Reviews
               </button>

               <div className="page-header">
                    <div>
                         <h2 className="page-title">{review.repo_name}</h2>
                         <div className="page-subtitle" style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                              <span>Pull Request #{review.pr_number}</span>
                              <span className={`badge ${review.status || 'completed'}`}>{review.status || 'completed'}</span>
                              <span>{findings.length} Findings</span>
                         </div>
                    </div>
               </div>

               {findings.length === 0 ? (
                    <div className="state-container">
                         <div style={{ fontSize: '48px', marginBottom: '16px', opacity: 0.9 }}>✅</div>
                         <div className="state-title">No issues found</div>
                         <div className="state-desc">The automated review completed successfully and did not identify any findings. Excellent work!</div>
                    </div>
               ) : (
                    <>
                         <div className="metrics-grid">
                              <div className="metric-card" style={{ borderTop: '4px solid var(--danger)' }}>
                                   <div className="metric-label">High Severity</div>
                                   <div className="metric-value">{highFindings}</div>
                              </div>
                              <div className="metric-card" style={{ borderTop: '4px solid var(--warning)' }}>
                                   <div className="metric-label">Medium Severity</div>
                                   <div className="metric-value">{mediumFindings}</div>
                              </div>
                              <div className="metric-card" style={{ borderTop: '4px solid var(--success)' }}>
                                   <div className="metric-label">Low Severity</div>
                                   <div className="metric-value">{lowFindings}</div>
                              </div>
                         </div>

                         <div style={{ marginTop: '2rem' }}>
                              {findings.map((finding) => (
                                   <div key={finding.id} className="finding-item">
                                        <div className="finding-header">
                                             <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                                                  <span className={`badge ${finding.severity.toLowerCase()}`}>
                                                       {finding.severity}
                                                  </span>
                                                  <span style={{ fontSize: '12px', fontWeight: '500', color: 'var(--text-primary)' }}>
                                                       {finding.category}
                                                  </span>
                                             </div>
                                             <div className="finding-meta">
                                                  {finding.source}
                                             </div>
                                        </div>
                                        
                                        <div className="finding-body">
                                             <div className="finding-file-loc">
                                                  📄 {finding.file_path}
                                                  <span className="finding-line">Line {finding.line_number}</span>
                                             </div>
                                             
                                             <div className="finding-message">
                                                  {finding.message}
                                             </div>

                                             {finding.suggested_fix && (
                                                  <div className="finding-fix">
                                                       <div className="finding-fix-title">Suggested Fix</div>
                                                       <div className="finding-fix-content">{finding.suggested_fix}</div>
                                                  </div>
                                             )}
                                        </div>
                                   </div>
                              ))}
                         </div>
                    </>
               )}
          </div>
     );
}