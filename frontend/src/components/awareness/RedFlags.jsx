import "./RedFlags.css";
import { phishingRedFlags } from "../../Data/awarenessData";

function RedFlags() {
  return (
    <div className="redflags-card">

      <h3>🚩 Red Flags in a Phishing Email</h3>

      <p className="redflags-subtitle">
        Learn to identify common warning signs before clicking suspicious
        emails or links.
      </p>

      <div className="redflags-grid">

        {phishingRedFlags.map((flag) => (

          <div className="redflag-item" key={flag.id}>

            <div className="redflag-icon">

              {flag.icon}

            </div>

            <h4>{flag.title}</h4>

            <p>{flag.description}</p>

            <div className="redflag-example">

              <strong>Example</strong>

              <span>{flag.example}</span>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

export default RedFlags;