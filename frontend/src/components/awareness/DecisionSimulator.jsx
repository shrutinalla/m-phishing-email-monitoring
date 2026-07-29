import { useState } from "react";
import "./DecisionSimulator.css";
import { decisionScenarios } from "../../Data/awarenessData";

function DecisionSimulator() {
  const [currentScenario, setCurrentScenario] = useState(0);
  const [selectedAction, setSelectedAction] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const scenario = decisionScenarios[currentScenario];

  const handleSubmit = () => {
    if (selectedAction === null) return;

    if (selectedAction === scenario.correctAction) {
      setScore((prev) => prev + 1);
    }

    setSubmitted(true);
  };

  const handleNext = () => {
    if (currentScenario < decisionScenarios.length - 1) {
      setCurrentScenario((prev) => prev + 1);
      setSelectedAction(null);
      setSubmitted(false);
    }
  };

  const handleRestart = () => {
    setCurrentScenario(0);
    setSelectedAction(null);
    setSubmitted(false);
    setScore(0);
  };

  const finished =
    currentScenario === decisionScenarios.length - 1 && submitted;

  return (
    <div className="decision-card">

      {finished ? (

        <div className="decision-result">

          <h2>🎉 Simulation Completed</h2>

          <h3>
            Score: {score} / {decisionScenarios.length}
          </h3>

          <button
            className="decision-btn"
            onClick={handleRestart}
          >
            Restart Simulation
          </button>

        </div>

      ) : (

        <>

          <div className="decision-header">

            <h2>Email Decision Simulator</h2>

            <span>
              Scenario {currentScenario + 1} of {decisionScenarios.length}
            </span>

          </div>

          <div className="decision-email">

            <p><strong>From:</strong> {scenario.sender}</p>

            <p><strong>Subject:</strong> {scenario.subject}</p>

            <hr />

            <p>{scenario.body}</p>

          </div>

          <div className="decision-actions">

            {scenario.actions.map((action, index) => (

              <button
                key={index}
                className={`decision-option
                  ${selectedAction === index ? "selected" : ""}
                  ${
                    submitted && index === scenario.correctAction
                      ? "correct"
                      : ""
                  }
                  ${
                    submitted &&
                    selectedAction === index &&
                    selectedAction !== scenario.correctAction
                      ? "wrong"
                      : ""
                  }`}
                disabled={submitted}
                onClick={() => setSelectedAction(index)}
              >
                {action}
              </button>

            ))}

          </div>

          {!submitted ? (

            <button
              className="decision-btn"
              onClick={handleSubmit}
            >
              Submit Decision
            </button>

          ) : (

            <>

              <div className="decision-explanation">

                <strong>Explanation</strong>

                <p>{scenario.explanation}</p>

              </div>

              <button
                className="decision-btn"
                onClick={handleNext}
              >
                Next Scenario
              </button>

            </>

          )}

        </>

      )}

    </div>
  );
}

export default DecisionSimulator;