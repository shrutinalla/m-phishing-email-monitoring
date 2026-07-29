import "./WarningPage.css";

function WarningPage() {
  return (
    <div className="warning-page">
      <div className="warning-card">

        <div className="warning-icon">⚠️</div>

        <h1>Security Awareness Simulation</h1>

        <p className="warning-message">
          This email was part of an authorized phishing awareness campaign.
        </p>

        <div className="success-box">
          <h2>Click Recorded Successfully</h2>

          <p>
            Your interaction has been recorded for security awareness
            training purposes.
          </p>
        </div>

        <div className="tips-section">

          <h3>How to Identify Phishing Emails</h3>

          <ul>

            <li>Verify the sender's email address.</li>

            <li>Hover over links before clicking.</li>

            <li>Avoid opening unexpected attachments.</li>

            <li>Do not share passwords through email.</li>

            <li>Report suspicious emails to your IT team.</li>

          </ul>

        </div>

        <div className="footer-note">
          <p>
            Stay alert. Think before you click.
          </p>

          <span>MIDHANI Security Awareness Program</span>
        </div>

      </div>
    </div>
  );
}

export default WarningPage;