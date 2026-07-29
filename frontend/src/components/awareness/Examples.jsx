import "./Examples.css";
import { phishingExamples } from "../../Data/awarenessData";

function Examples() {
  return (
    <section className="examples-section">

      <div className="section-header">
        <h2>Phishing Email Examples</h2>
        <p>
          Learn how to recognize phishing attempts by analyzing realistic
          examples and identifying their warning signs.
        </p>
      </div>

      <div className="examples-container">

        {phishingExamples.map((example) => (

          <div className="example-card" key={example.id}>

            <div className="example-top">

              <span className={`difficulty ${example.difficulty.toLowerCase()}`}>
                {example.difficulty}
              </span>

            </div>

            <div className="email-preview">

              <div className="email-header">

                <p>
                  <strong>From:</strong> {example.sender}
                </p>

                <p>
                  <strong>Subject:</strong> {example.subject}
                </p>

              </div>

              <div className="email-body">

                {example.body.split("\n").map((line, index) => (
                  <p key={index}>{line}</p>
                ))}

              </div>

            </div>

            <div className="warning-section">

              <h4>⚠ Warning Signs</h4>

              <ul>

                {example.warningSigns.map((warning, index) => (
                  <li key={index}>{warning}</li>
                ))}

              </ul>

            </div>

            <div className="example-explanation">

              <h4>Why is this suspicious?</h4>

              <p>{example.explanation}</p>

            </div>

          </div>

        ))}

      </div>

    </section>
  );
}

export default Examples;