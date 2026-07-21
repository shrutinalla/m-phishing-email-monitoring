import DashboardLayout from "../../components/layout/DashboardLayout";
import {
  FaUsers,
  FaEnvelope,
  FaMousePointer,
  FaShieldAlt,
  FaArrowUp,
} from "react-icons/fa";
import "./Dashboard.css";

const recentCampaigns = [
  {
    name: "Fake HR Policy Update",
    status: "Completed",
    date: "20 Jul 2026",
  },
  {
    name: "Password Reset Alert",
    status: "Running",
    date: "19 Jul 2026",
  },
  {
    name: "VPN Configuration",
    status: "Completed",
    date: "17 Jul 2026",
  },
];

function Dashboard() {
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
              <h2>245</h2>
              <span>Total Employees</span>
            </div>

          </div>

          <div className="stat-card">

            <div className="icon campaign">
              <FaEnvelope />
            </div>

            <div>
              <h2>18</h2>
              <span>Campaigns</span>
            </div>

          </div>

          <div className="stat-card">

            <div className="icon clicks">
              <FaMousePointer />
            </div>

            <div>
              <h2>42</h2>
              <span>Phishing Clicks</span>
            </div>

          </div>

          <div className="stat-card">

            <div className="icon security">
              <FaShieldAlt />
            </div>

            <div>
              <h2>82%</h2>
              <span>Security Score</span>
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

                {recentCampaigns.map((campaign, index) => (

                  <tr key={index}>

                    <td>{campaign.name}</td>

                    <td>

                      <span
                        className={
                          campaign.status === "Running"
                            ? "status running"
                            : "status completed"
                        }
                      >
                        {campaign.status}
                      </span>

                    </td>

                    <td>{campaign.date}</td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

          <div className="activity-card">

            <h2>Security Overview</h2>

            <div className="circle">

              <h1>82%</h1>

              <span>Protected</span>

            </div>

            <div className="overview-row">

              <span>
                <FaArrowUp />
                Awareness Score
              </span>

              <strong>Excellent</strong>

            </div>

            <div className="overview-row">

              <span>Emails Sent</span>

              <strong>1250</strong>

            </div>

            <div className="overview-row">

              <span>Clicks Recorded</span>

              <strong>42</strong>

            </div>

            <div className="overview-row">

              <span>Departments Covered</span>

              <strong>8</strong>

            </div>

          </div>

        </div>

      </div>
    </DashboardLayout>
  );
}

export default Dashboard;