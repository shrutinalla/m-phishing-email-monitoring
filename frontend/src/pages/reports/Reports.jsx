import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import "./Reports.css";

function Reports() {

  const [statusFilter, setStatusFilter] = useState("All");
  const [search, setSearch] = useState("");

  const reportStats = [
    {
      title: "Total Campaigns",
      value: 28,
      icon: "📧"
    },
    {
      title: "Running",
      value: 4,
      icon: "🟡"
    },
    {
      title: "Completed",
      value: 20,
      icon: "✅"
    },
    {
      title: "Failed",
      value: 4,
      icon: "❌"
    }
  ];

  const campaigns = [
    {
      id:1,
      campaign:"Password Reset",
      department:"IT",
      template:"Password Reset",
      sent:120,
      opened:82,
      clicked:38,
      credentials:9,
      risk:82,
      status:"Completed"
},
    {
      id:2,
      campaign:"Salary Slip",
      department:"Finance",
      template:"Salary Slip",
      sent:75,
      opened:55,
      clicked:12,
      credentials:2,
      risk:45,
      status:"Running"
    },
    {
      id:3,
      campaign:"VPN Renewal",
      department:"Production",
      template:"VPN",
      sent:96,
      opened:70,
      clicked:29,
      credentials:6,
      risk:63,
      status:"Scheduled"
    }
  ];

  const recentActivities = [
    "Password Reset campaign completed",
    "VPN campaign scheduled",
    "Finance campaign created",
    "15 employees clicked phishing link",
    "Credential submission detected"
  ];

  return (

    <DashboardLayout>

      <div className="reports-page">

        <div className="reports-header">

          <div>

            <h1>Campaign Reports</h1>

            <p>
              View phishing campaign statistics, employee engagement and security metrics.
            </p>

          </div>

          <button className="export-btn">

            Export CSV

          </button>

        </div>
                {/* ===================== KPI CARDS ===================== */}

        <div className="stats-grid">

          {reportStats.map((stat) => (

            <div
              key={stat.title}
              className="stat-card"
            >

              <div className="stat-icon">
                {stat.icon}
              </div>

              <div>

                <h2>{stat.value}</h2>

                <p>{stat.title}</p>

              </div>

            </div>

          ))}

        </div>

        {/* ===================== SEARCH & FILTER ===================== */}

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
              <option>Running</option>
              <option>Scheduled</option>
              <option>Completed</option>
              <option>Failed</option>

            </select>

          </div>

        </div>

        {/* ===================== CAMPAIGN TABLE ===================== */}
        <div className="table-card">
          
          <h3>Campaign Summary</h3>
          
          <div className="table-wrapper">
            
            <table className="reports-table">     

            <thead>

              <tr>

                <th>Campaign</th>
                
                <th>Department</th>
                
                <th>Template</th>
                
                <th>Sent</th>
                
                <th>Opened</th>
                
                <th>Clicked</th>
                
                <th>Credentials Submitted</th>
                
                <th>Risk Score</th>
                
                <th>Status</th>
                
                <th>Action</th>

              </tr>

            </thead>

            <tbody>

              

              {campaigns
                .filter((item) => {

                  const matchesSearch =
                    item.campaign
                      .toLowerCase()
                      .includes(search.toLowerCase());

                  const matchesStatus =
                    statusFilter === "All"
                      ? true
                      : item.status === statusFilter;

                  return matchesSearch && matchesStatus;

                })
                .map((item) => (

                  <tr key={item.id}>

                    <td>{item.campaign}</td>

                    <td>{item.department}</td>

                    <td>{item.template}</td>

                    <td>{item.sent}</td>
                    
                    <td>{item.opened}</td>
                    
                    <td>{item.clicked}</td>
                    
                    <td>{item.credentials}</td>
                    
                    <td>{item.risk}%</td>

                    <td>

                      <span
                        className={`status ${item.status.toLowerCase()}`}
                      >
                        {item.status}
                      </span>

                    </td>

                    <td>

                      <button className="view-btn">

                        View

                      </button>

                    </td>

                  </tr>

                ))}

            </tbody>

          </table>

          </div>

        </div>
                {/* ===================== TREND ANALYTICS ===================== */}

        <div className="trend-card">

          <h3>Campaign Trend Analysis</h3>

          <div className="trend-bars">

            <div className="trend-item">

              <span>Jan</span>

              <div className="bar">

                <div
                  className="fill"
                  style={{ width: "45%" }}
                ></div>

              </div>

            </div>

            <div className="trend-item">

              <span>Feb</span>

              <div className="bar">

                <div
                  className="fill"
                  style={{ width: "70%" }}
                ></div>

              </div>

            </div>

            <div className="trend-item">

              <span>Mar</span>

              <div className="bar">

                <div
                  className="fill"
                  style={{ width: "90%" }}
                ></div>

              </div>

            </div>

            <div className="trend-item">

              <span>Apr</span>

              <div className="bar">

                <div
                  className="fill"
                  style={{ width: "60%" }}
                ></div>

              </div>

            </div>

          </div>

        </div>

        {/* ===================== RECENT ACTIVITY ===================== */}

        <div className="activity-card">

          <h3>Recent Activity</h3>

          <div className="activity-list">

            {recentActivities.map((activity, index) => (

              <div
                key={index}
                className="activity-item"
              >

                <div className="activity-dot"></div>

                <p>{activity}</p>

              </div>

            ))}

          </div>

        </div>

      </div>

    </DashboardLayout>

  );

}

export default Reports;