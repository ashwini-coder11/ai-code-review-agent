import { useEffect, useState } from "react";
import {
     BarChart,
     Bar,
     XAxis,
     YAxis,
     Tooltip,
     PieChart,
     Pie,
     Cell,
     LineChart,
     Line,
     ResponsiveContainer,
} from "recharts";
import { getSummary, getTimeline } from "../api";

// Recharts colors from our design system
const COLORS = ['#4F8CFF', '#e3b341', '#3fb950', '#f85149', '#8B95A5'];

export default function Analytics() {
     const [summary, setSummary] = useState(null);
     const [timeline, setTimeline] = useState([]);
     const [loading, setLoading] = useState(true);
     const [error, setError] = useState(null);

     useEffect(() => {
          Promise.all([getSummary(), getTimeline()])
               .then(([summaryData, timelineData]) => {
                    setSummary(summaryData);
                    setTimeline(timelineData);
               })
               .catch(() => setError("Failed to load analytics."))
               .finally(() => setLoading(false));
     }, []);

     if (loading) {
          return (
               <div className="state-container">
                    <div className="state-title">Loading analytics...</div>
               </div>
          );
     }

     if (error) {
          return (
               <div className="state-container error-container">
                    <div className="state-title">Unable to load analytics</div>
                    <div className="state-desc">{error}</div>
                    <button className="btn btn-secondary" onClick={() => window.location.reload()}>Retry</button>
               </div>
          );
     }

     const categoryData = Object.entries(summary?.by_category || {}).map(
          ([name, value]) => ({ name, value })
     );

     const sourceData = Object.entries(summary?.by_source || {}).map(
          ([name, value]) => ({ name, value })
     );
     
     // Handle empty analytics data
     const hasData = categoryData.length > 0 || sourceData.length > 0 || timeline.length > 0;

     return (
          <div>
               <div className="page-header">
                    <div>
                         <h2 className="page-title">Analytics</h2>
                         <div className="page-subtitle">Understand review activity and code quality trends.</div>
                    </div>
               </div>

               {!hasData ? (
                    <div className="state-container">
                         <div style={{ fontSize: '48px', marginBottom: '16px', opacity: 0.9 }}>📊</div>
                         <div className="state-title">No data available</div>
                         <div className="state-desc">Analytics will populate here once pull request reviews have been processed.</div>
                    </div>
               ) : (
                    <>
                         <div className="charts-grid">
                              <div className="card">
                                   <h3 className="card-title">Findings by Category</h3>
                                   <div style={{ height: 300, width: '100%' }}>
                                        {categoryData.length > 0 ? (
                                             <ResponsiveContainer>
                                                  <BarChart data={categoryData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                                       <XAxis dataKey="name" tick={{ fill: 'var(--text-secondary)' }} tickLine={false} axisLine={{ stroke: 'var(--border)' }} />
                                                       <YAxis tick={{ fill: 'var(--text-secondary)' }} tickLine={false} axisLine={{ stroke: 'var(--border)' }} />
                                                       <Tooltip contentStyle={{ backgroundColor: 'var(--surface-elevated)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)' }} />
                                                       <Bar dataKey="value" fill="var(--accent)" radius={[4, 4, 0, 0]} />
                                                  </BarChart>
                                             </ResponsiveContainer>
                                        ) : (
                                             <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>No category data</div>
                                        )}
                                   </div>
                              </div>

                              <div className="card">
                                   <h3 className="card-title">Static vs LLM Findings</h3>
                                   <div style={{ height: 300, width: '100%' }}>
                                        {sourceData.length > 0 ? (
                                             <ResponsiveContainer>
                                                  <PieChart>
                                                       <Pie
                                                            data={sourceData}
                                                            dataKey="value"
                                                            nameKey="name"
                                                            cx="50%"
                                                            cy="50%"
                                                            innerRadius={60}
                                                            outerRadius={100}
                                                            labelLine={false}
                                                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                                       >
                                                            {sourceData.map((entry, index) => (
                                                                 <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                            ))}
                                                       </Pie>
                                                       <Tooltip contentStyle={{ backgroundColor: 'var(--surface-elevated)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)' }} />
                                                  </PieChart>
                                             </ResponsiveContainer>
                                        ) : (
                                             <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>No source data</div>
                                        )}
                                   </div>
                              </div>
                         </div>

                         <div className="card">
                              <h3 className="card-title">Review Volume Over Time</h3>
                              <div style={{ height: 300, width: '100%' }}>
                                   {timeline.length > 0 ? (
                                        <ResponsiveContainer>
                                             <LineChart data={timeline} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                                  <XAxis dataKey="date" tick={{ fill: 'var(--text-secondary)' }} tickLine={false} axisLine={{ stroke: 'var(--border)' }} />
                                                  <YAxis tick={{ fill: 'var(--text-secondary)' }} tickLine={false} axisLine={{ stroke: 'var(--border)' }} />
                                                  <Tooltip contentStyle={{ backgroundColor: 'var(--surface-elevated)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)' }} />
                                                  <Line type="monotone" dataKey="count" stroke="var(--accent)" strokeWidth={3} dot={{ fill: 'var(--surface)', stroke: 'var(--accent)', strokeWidth: 2, r: 4 }} activeDot={{ r: 6 }} />
                                             </LineChart>
                                        </ResponsiveContainer>
                                   ) : (
                                        <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>No timeline data</div>
                                   )}
                              </div>
                         </div>
                    </>
               )}
          </div>
     );
}