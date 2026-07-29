import "./Completion.css";
import { completionSummary } from "../../Data/awarenessData";

function Completion() {
  return (
    <section className="completion-card">

      <div className="completion-header">

        <h2>🎉 {completionSummary.title}</h2>

        <p>{completionSummary.message}</p>

      </div>

      <div className="completion-grid">

        <div className="completion-box">

          <h3>Achievements</h3>

          <ul>
            {completionSummary.achievements.map((item, index) => (
              <li key={index}>✅ {item}</li>
            ))}
          </ul>

        </div>

        <div className="completion-box">

          <h3>Security Reminders</h3>

          <ul>
            {completionSummary.reminders.map((item, index) => (
              <li key={index}>🔒 {item}</li>
            ))}
          </ul>

        </div>

      </div>

      <div className="completion-footer">

        <button
          className="completion-btn"
          onClick={() => window.location.href="/dashboard"}
        >
          Return to Dashboard
        </button>

      </div>

    </section>
  );
}

export default Completion;