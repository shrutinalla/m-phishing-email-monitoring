import DashboardLayout from "../../components/layout/DashboardLayout";
import Timeline from "../../components/awareness/Timeline";
import RedFlags from "../../components/awareness/RedFlags";
import Quiz from "../../components/awareness/Quiz";
import Examples from "../../components/awareness/Examples";
import DecisionSimulator from "../../components/awareness/DecisionSimulator";
import Completion from "../../components/awareness/Completion";
import "./Awareness.css";

import {
  awarenessStats,
  awarenessModules,
} from "../../Data/awarenessData";

function AwarenessPage() {

 

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

          {awarenessStats.map((item) => (

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

  <Timeline />
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

        <Quiz />

        <Examples />

        <DecisionSimulator />

        
        {/* ================= NOTIFICATIONS ================= */}

       <RedFlags />

       <Completion />
        {/* ================= RESOURCES ================= */}

        <div className="resources-card">

          <div className="card-header">

            <h3>Learning Resources</h3>

          </div>

         <div className="resource-grid">

  <button
    className="resource-btn"
    onClick={() =>
      window.open("/resources/phishing-awareness-guide.pdf", "_blank")
    }
  >
    📄 Phishing Awareness Guide
  </button>

  <button
    className="resource-btn"
    onClick={() =>
      window.open("/resources/security-best-practices.pdf", "_blank")
    }
  >
    📘 Security Best Practices
  </button>

  <button
    className="resource-btn"
    onClick={() =>
      window.open(
        "https://www.youtube.com/results?search_query=phishing+awareness+training",
        "_blank"
      )
    }
  >
    🎥 Awareness Training Video
  </button>

  <button
    className="resource-btn"
    onClick={() =>
      window.open("/resources/security-handbook.pdf", "_blank")
    }
  >
    📥 Download Security Handbook
  </button>

</div>

        </div>

      </div>

    </DashboardLayout>

  );

}

export default AwarenessPage; 