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
import { getDashboard } from "../../services/dashboardService";


  function Dashboard() {

  const [stats, setStats] = useState({
    total_employees: 0,
    clicked: 0,
    high_risk: 0,
    safe: 0,
  });

  const loadDashboard = async () => {
    try {
      const data = await getDashboard();
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
              <h2>{stats.safe}</h2>
              <span>Safe Employees</span>
            </div>

          </div>

        </div>

        <div className="dashboard-content">

          <div className="table-card">

            <div className="section-title">

              <h2>Recent Campaigns</h2>

              <button>View All</button>

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

    <h1>--</h1>

    <span>No Data Yet</span>

  </div>

  <div className="overview-row">

    <span>
      <FaArrowUp />
      Awareness Score
    </span>

    <strong>--</strong>

  </div>

  <div className="overview-row">

    <span>Emails Sent</span>

    <strong>--</strong>

  </div>

  <div className="overview-row">

    <span>Clicks Recorded</span>

    <strong>--</strong>

  </div>

  <div className="overview-row">

    <span>Departments Covered</span>

    <strong>--</strong>

  </div>

</div>

        </div>

      </div>
    </DashboardLayout>
  );
}

export default Dashboard;