import { useState, useEffect } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import CampaignDetailsModal from "../../components/reports/CampaignDetailsModal";
import {
  getReports,
  getCampaignDetails,
  exportReports,
} from "../../services/reportService";
import "./Reports.css";

function Reports() {
  const [statusFilter, setStatusFilter] = useState("All");
  const [search, setSearch] = useState("");

  const [summary, setSummary] = useState({});
  const [campaigns, setCampaigns] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);

  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchReports = async () => {
    try {
      setLoading(true);

      const data = await getReports();

      setSummary(data.summary);
      setCampaigns(data.campaign_reports);

      const activities = data.campaign_reports
        .slice(0, 5)
        .map(
          (campaign) =>
            `${campaign.campaign_name} (${campaign.status}) - ${campaign.emails_clicked} click(s)`
        );

      setRecentActivities(activities);
    } catch (err) {
      console.error(err);
      setError("Failed to load reports.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleExportCSV = () => {
    exportReports();
  };

  const handleViewCampaign = async (campaignId) => {
    try {
      const data = await getCampaignDetails(campaignId);

      setSelectedCampaign(data);

      setShowModal(true);
    } catch (err) {
      console.error(err);
      alert("Failed to load campaign details.");
    }
  };

  const reportStats = [
    {
      title: "Campaigns",
      value: summary.total_campaigns ?? 0,
      icon: "📧",
    },
    {
      title: "Employees",
      value: summary.total_employees ?? 0,
      icon: "👥",
    },
    {
      title: "Clicked",
      value: summary.total_clicks ?? 0,
      icon: "🖱️",
    },
    {
      title: "Click Rate",
      value: `${summary.overall_click_rate ?? 0}%`,
      icon: "📈",
    },
  ];

  const filteredCampaigns = campaigns.filter((item) => {
    const query = search.toLowerCase();

    const matchesSearch =
      item.campaign_name?.toLowerCase().includes(query) ||
      item.email_subject?.toLowerCase().includes(query) ||
      item.difficulty?.toLowerCase().includes(query) ||
      item.status?.toLowerCase().includes(query);

    const matchesStatus =
      statusFilter === "All"
        ? true
        : item.status.toLowerCase() === statusFilter.toLowerCase();

    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <DashboardLayout>
        <div className="reports-page">
          <h2>Loading reports...</h2>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="reports-page">
          <h2>{error}</h2>
        </div>
      </DashboardLayout>
    );
  }
  return (
    <DashboardLayout>
      <div className="reports-page">
        <div className="reports-header">
          <div>
            <h1>Campaign Reports</h1>

            <p>
              View phishing campaign statistics, employee engagement and
              security metrics.
            </p>
          </div>

          <button className="export-btn" onClick={handleExportCSV}>
            Export CSV
          </button>
        </div>

        <div className="stats-grid">
          {reportStats.map((stat) => (
            <div key={stat.title} className="stat-card">
              <div className="stat-icon">{stat.icon}</div>

              <div>
                <h2>{stat.value}</h2>
                <p>{stat.title}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="filter-card">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search Campaign..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="status-filter">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option>All</option>
              <option>Draft</option>
              <option>Running</option>
              <option>Scheduled</option>
              <option>Completed</option>
              <option>Failed</option>
            </select>
          </div>
        </div>
                <div className="table-card">
          <h3>Campaign Summary</h3>

          <div className="table-wrapper">
            <table className="reports-table">
              <thead>
                <tr>
                  <th>Campaign</th>
                  <th>Subject</th>
                  <th>Difficulty</th>
                  <th>Recipients</th>
                  <th>Sent</th>
                  <th>Failed</th>
                  <th>Clicked</th>
                  <th>Click Rate</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredCampaigns.length === 0 ? (
                  <tr>
                    <td colSpan="10" style={{ textAlign: "center" }}>
                      No campaigns found.
                    </td>
                  </tr>
                ) : (
                  filteredCampaigns.map((item) => (
                    <tr key={item.campaign_id}>
                      <td>{item.campaign_name}</td>

                      <td>{item.email_subject || "-"}</td>

                      <td>{item.difficulty}</td>

                      <td>{item.total_recipients}</td>

                      <td>{item.emails_sent}</td>

                      <td>{item.emails_failed}</td>

                      <td>{item.emails_clicked}</td>

                      <td>{item.click_rate}%</td>

                      <td>
                        <span
                          className={`status ${item.status.toLowerCase()}`}
                        >
                          {item.status}
                        </span>
                      </td>

                      <td>
                        <button
                          className="view-btn"
                          onClick={() =>
                            handleViewCampaign(item.campaign_id)
                          }
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="trend-card">
          <h3>Campaign Status Overview</h3>

          <div className="trend-bars">
            <div className="trend-item">
              <span>Draft</span>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${Math.min((summary.draft || 0) * 20, 100)}%`,
                  }}
                ></div>
              </div>

              <span>{summary.draft || 0}</span>
            </div>

            <div className="trend-item">
              <span>Running</span>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${Math.min((summary.running || 0) * 20, 100)}%`,
                  }}
                ></div>
              </div>

              <span>{summary.running || 0}</span>
            </div>

            <div className="trend-item">
              <span>Completed</span>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${Math.min((summary.completed || 0) * 20, 100)}%`,
                  }}
                ></div>
              </div>

              <span>{summary.completed || 0}</span>
            </div>

            <div className="trend-item">
              <span>Failed</span>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${Math.min((summary.failed || 0) * 20, 100)}%`,
                  }}
                ></div>
              </div>

              <span>{summary.failed || 0}</span>
            </div>
          </div>
        </div>

        <div className="activity-card">
          <h3>Recent Activity</h3>

          <div className="activity-list">
            {recentActivities.length === 0 ? (
              <p>No recent activity.</p>
            ) : (
              recentActivities.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-dot"></div>
                  <p>{activity}</p>
                </div>
              ))
            )}
          </div>
        </div>

        <CampaignDetailsModal
          open={showModal}
          onClose={() => setShowModal(false)}
          campaignData={selectedCampaign}
        />
      </div>
    </DashboardLayout>
  );
}

export default Reports;