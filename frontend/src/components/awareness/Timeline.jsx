import "./Timeline.css";

function Timeline() {
  const timelineSteps = [
    {
      id: 1,
      title: "Phishing Email Delivered",
      description:
        "A simulated phishing email is delivered to the employee's inbox.",
      icon: "📧",
    },
    {
      id: 2,
      title: "Employee Clicks the Link",
      description:
        "The employee interacts with the phishing link inside the email.",
      icon: "🖱️",
    },
    {
      id: 3,
      title: "Warning Page Displayed",
      description:
        "The system immediately warns the employee before any sensitive information is entered.",
      icon: "⚠️",
    },
    {
      id: 4,
      title: "Awareness Training",
      description:
        "The employee is guided through phishing awareness and security best practices.",
      icon: "🎓",
    },
    {
      id: 5,
      title: "Training Completed",
      description:
        "The employee completes the awareness session and becomes better prepared against phishing attacks.",
      icon: "✅",
    },
  ];

  return (
    <div className="timeline-card">

      <h3>Phishing Simulation Workflow</h3>

      <div className="timeline-container">

        {timelineSteps.map((step, index) => (

          <div className="timeline-item" key={step.id}>

            <div className="timeline-icon">

              {step.icon}

            </div>

            <div className="timeline-content">

              <h4>{step.title}</h4>

              <p>{step.description}</p>

            </div>

            {index !== timelineSteps.length - 1 && (

              <div className="timeline-line"></div>

            )}

          </div>

        ))}

      </div>

    </div>
  );
}

export default Timeline;