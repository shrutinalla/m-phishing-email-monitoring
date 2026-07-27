import DashboardLayout from "../../components/layout/DashboardLayout";
import "./Awareness.css";

function AwarenessPage() {

  const stats = [
    {
      title: "Employees Trained",
      value: "182",
      icon: "🎓"
    },
    {
      title: "Completion Rate",
      value: "84%",
      icon: "✅"
    },
    {
      title: "Pending Training",
      value: "34",
      icon: "⏳"
    },
    {
      title: "Average Quiz Score",
      value: "88%",
      icon: "📊"
    }
  ];

  const modules = [
    {
      id: 1,
      title: "Recognizing Phishing Emails",
      duration: "15 mins",
      level: "Beginner",
      status: "Completed"
    },
    {
      id: 2,
      title: "Credential Theft Awareness",
      duration: "20 mins",
      level: "Intermediate",
      status: "In Progress"
    },
    {
      id: 3,
      title: "Safe Link Verification",
      duration: "12 mins",
      level: "Beginner",
      status: "Pending"
    },
    {
      id: 4,
      title: "Email Security Best Practices",
      duration: "18 mins",
      level: "Advanced",
      status: "Pending"
    }
  ];

  return (

    <DashboardLayout>

      <div className="awareness-page">

        {/* ================= HEADER ================= */}

        <div className="awareness-header">

          <div>

            <h1>Security Awareness & Training</h1>

            <p>
              Strengthen employee awareness through phishing education,
              security training and interactive learning modules.
            </p>

          </div>

          <button className="assign-btn">

            Assign Training

          </button>

        </div>

        {/* ================= KPI CARDS ================= */}

        <div className="stats-grid">

          {stats.map((item) => (

            <div
              key={item.title}
              className="stat-card"
            >

              <div className="stat-icon">

                {item.icon}

              </div>

              <div>

                <h2>{item.value}</h2>

                <p>{item.title}</p>

              </div>

            </div>

          ))}

        </div>

        {/* ================= TRAINING MODULES ================= */}

        <div className="modules-card">

          <div className="card-header">

            <h3>Training Modules</h3>

            <button className="view-all-btn">

              View All

            </button>

          </div>

          <table className="modules-table">

            <thead>

              <tr>

                <th>Module</th>

                <th>Duration</th>

                <th>Difficulty</th>

                <th>Status</th>

              </tr>

            </thead>

            <tbody>

              {modules.map((module) => (

                <tr key={module.id}>

                  <td>{module.title}</td>

                  <td>{module.duration}</td>

                  <td>{module.level}</td>

                  <td>

                    <span
                      className={`status ${module.status
                        .toLowerCase()
                        .replace(/\s/g, "-")}`}
                    >

                      {module.status}

                    </span>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>
               {/* ================= SECURITY TIPS ================= */}

        <div className="tips-card">

          <h3>Daily Security Tips</h3>

          <div className="tips-list">

            <div className="tip-item">
              <span>🛡️</span>
              <p>Always verify the sender's email address before opening attachments.</p>
            </div>

            <div className="tip-item">
              <span>🔒</span>
              <p>Never share your passwords through email or messaging platforms.</p>
            </div>

            <div className="tip-item">
              <span>⚠️</span>
              <p>Hover over links before clicking to verify the destination URL.</p>
            </div>

            <div className="tip-item">
              <span>📧</span>
              <p>Report suspicious emails immediately to your security team.</p>
            </div>

          </div>

        </div>

        {/* ================= QUIZ ================= */}

        <div className="quiz-card">

          <div className="card-header">

            <h3>Quick Security Quiz</h3>

            <button className="start-btn">

              Start Quiz

            </button>

          </div>

          <div className="quiz-content">

            <h4>
              Which of the following is a common sign of a phishing email?
            </h4>

            <div className="quiz-options">

              <label>

                <input type="radio" name="quiz" />

                Urgent request for confidential information

              </label>

              <label>

                <input type="radio" name="quiz" />

                Email from verified internal HR

              </label>

              <label>

                <input type="radio" name="quiz" />

                Scheduled meeting invitation

              </label>

              <label>

                <input type="radio" name="quiz" />

                Company newsletter

              </label>

            </div>

          </div>

        </div>

        {/* ================= NOTIFICATIONS ================= */}

        <div className="notification-card">

          <h3>Recent Awareness Updates</h3>

          <div className="notification-list">

            <div className="notification-item">

              <div className="dot"></div>

              <p>Monthly phishing awareness campaign launched.</p>

            </div>

            <div className="notification-item">

              <div className="dot"></div>

              <p>Credential Theft Awareness module updated.</p>

            </div>

            <div className="notification-item">

              <div className="dot"></div>

              <p>Quarterly security assessment scheduled.</p>

            </div>

            <div className="notification-item">

              <div className="dot"></div>

              <p>Password hygiene reminder sent to all employees.</p>

            </div>

          </div>

        </div>

        {/* ================= RESOURCES ================= */}

        <div className="resources-card">

          <div className="card-header">

            <h3>Learning Resources</h3>

          </div>

          <div className="resource-grid">

            <button className="resource-btn">

              📄 Phishing Awareness Guide

            </button>

            <button className="resource-btn">

              📘 Security Best Practices

            </button>

            <button className="resource-btn">

              🎥 Awareness Training Video

            </button>

            <button className="resource-btn">

              📥 Download Security Handbook

            </button>

          </div>

        </div>

      </div>

    </DashboardLayout>

  );

}

export default AwarenessPage; 