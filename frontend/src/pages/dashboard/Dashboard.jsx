import DashboardLayout from "../../components/layout/DashboardLayout";
import {
  FaUsers,
  FaEnvelope,
  FaMousePointer,
  FaShieldAlt,
  FaArrowUp,
} from "react-icons/fa";
import "./Dashboard.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getDashboard } from "../../services/dashboardService";
import routes from "../../utils/routes";
  function Dashboard() {

  const [stats, setStats] = useState({

    total_employees:0,

    total_campaigns:0,

    running_campaigns:0,

    completed_campaigns:0,

    emails_sent:0,

    emails_failed:0,

    total_clicks:0,

    click_rate:0,

    high_risk_employees:0

});
const navigate = useNavigate();
  const loadDashboard = async () => {
    try {
      const data = await getDashboard();
      console.log("Dashboard API Response:", data);
      setStats(data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);
  return (
    <DashboardLayout>
      <div className="dashboard">

        <div className="dashboard-header">

          <div>
            <h1>Dashboard</h1>

            <p>
              Welcome back, Administrator.
              Monitor phishing campaigns and employee awareness
              from one place.
            </p>
          </div>

        </div>

        <div className="stats-grid">

          <div className="stat-card">

            <div className="icon users">
              <FaUsers />
            </div>

            <div>
              <h2>{stats.total_employees}</h2>
              <span>Total Employees</span>
            </div>

          </div>

          <div className="stat-card">

            <div className="icon campaign">
              <FaEnvelope />
            </div>

            <div>
              <h2>{stats.high_risk}</h2>
              <span>High Risk</span>
            </div>

          </div>

          <div className="stat-card">

            <div className="icon clicks">
              <FaMousePointer />
            </div>

            <div>
              <h2>{stats.clicked}</h2>
              <span>Phishing Clicks</span>
            </div>

          </div>

          <div className="stat-card">

            <div className="icon security">
              <FaShieldAlt />
            </div>

            <div>
              <h2>
  {stats.safe}
</h2>
              <span>Safe Employees</span>
            </div>

          </div>

        </div>

        <div className="dashboard-content">

          <div className="table-card">

            <div className="section-title">

              <h2>Recent Campaigns</h2>

              <button onClick={() => navigate(routes.REPORTS)}>
  View All
</button>

            </div>

            <table>

              <thead>

                <tr>

                  <th>Campaign</th>
                  <th>Status</th>
                  <th>Date</th>

                </tr>

              </thead>

              <tbody>

  <tr>
    <td
      colSpan="3"
      style={{
        textAlign: "center",
        padding: "40px",
        color: "#6b7280",
      }}
    >
      No campaigns have been created yet.
    </td>
  </tr>

</tbody>

            </table>

          </div>

         <div className="activity-card">

  <h2>Security Overview</h2>

  <div className="circle">

    <h1>
  {stats.total_employees > 0
    ? Math.round(
        (stats.safe/stats.total_employees) *
          100
      )
    : 0}
%
</h1>

    <span>Security Score</span>

  </div>

  <div className="overview-row">

  <span>
    <FaArrowUp />
    Awareness Score
  </span>

  <strong>
    {stats.total_employees > 0
      ? Math.round(
          ((stats.safe) /
stats.total_employees) *
            100
        ) + "%"
      : "0%"}
  </strong>

</div>

  <div className="overview-row">

  <span>Total Campaigns</span>

  <strong>{stats.total_campaigns}</strong>

</div>

  <div className="overview-row">

  <span>Emails Sent</span>

  <strong>{stats.emails_sent}</strong>

</div>

  <div className="overview-row">

  <span>Click Rate</span>

  <strong>{stats.click_rate}%</strong>

</div>
<div className="overview-row">

  <span>Running Campaigns</span>

  <strong>{stats.running_campaigns}</strong>

</div>

<div className="overview-row">

  <span>Completed Campaigns</span>

  <strong>{stats.completed_campaigns}</strong>

</div>

</div>

              </div>

        <div className="quick-actions">

          <h2>Quick Actions</h2>

          <div className="quick-grid">

            <button
              className="quick-card"
              onClick={() => navigate(routes.CAMPAIGNS)}
            >
              <span className="quick-icon">📧</span>
              <h3>Create Campaign</h3>
              <p>Launch a phishing simulation.</p>
            </button>

            <button
              className="quick-card"
              onClick={() => navigate(routes.EMPLOYEES)}
            >
              <span className="quick-icon">👥</span>
              <h3>Employees</h3>
              <p>Manage employee records.</p>
            </button>

            <button
              className="quick-card"
              onClick={() => navigate(routes.REPORTS)}
            >
              <span className="quick-icon">📊</span>
              <h3>Reports</h3>
              <p>View campaign analytics.</p>
            </button>

            <button
              className="quick-card"
              onClick={() => navigate(routes.AWARENESS)}
            >
              <span className="quick-icon">🛡️</span>
              <h3>Awareness</h3>
              <p>Open security training.</p>
            </button>

          </div>

        </div>

      </div>
    </DashboardLayout>  
  );
}

export default Dashboard;