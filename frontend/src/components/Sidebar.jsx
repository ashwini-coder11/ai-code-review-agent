import { NavLink } from "react-router-dom";

export default function Sidebar() {
     return (
          <aside className="sidebar">
               <div className="sidebar-header">
                    <div className="sidebar-brand">AI CODE REVIEWER</div>
                    <div className="sidebar-subtitle">AI-powered Pull Request Analysis</div>
               </div>

               <nav className="sidebar-nav">
                    <NavLink to="/" end className="nav-link">
                         Reviews
                    </NavLink>
                    <NavLink to="/analytics" className="nav-link">
                         Analytics
                    </NavLink>
               </nav>

               <div className="sidebar-footer">
                    <div className="system-status">
                         <div className="status-indicator"></div>
                         System Online
                    </div>
               </div>
          </aside>
     );
}
