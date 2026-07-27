import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import "./ComposeCampaign.css";
import { getEmployees } from "../../services/employeeService";
import { getTemplates, getTemplate } from "../../services/templateService";
import {
  createCampaign,
  sendCampaign,
} from "../../services/campaignService";

function ComposeCampaign() {
  const [difficulty, setDifficulty] = useState("Medium");
  const [template, setTemplate] = useState("Password Reset");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [department, setDepartment] = useState("All Departments");
  const [search, setSearch] = useState("");
  const [schedule, setSchedule] = useState("now");
  const [attachment, setAttachment] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
const [employees, setEmployees] = useState([]);
const [templates, setTemplates] = useState([]);
const [selectedEmployees, setSelectedEmployees] = useState([]);
const [selectedTemplate, setSelectedTemplate] = useState(null);


  const filteredEmployees = employees.filter((employee) =>
  employee.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
  employee.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
  employee.department.toLowerCase().includes(searchTerm.toLowerCase())
);
const handleEmployeeSelection = (employeeId) => {

  if (selectedEmployees.includes(employeeId)) {

    setSelectedEmployees(
      selectedEmployees.filter(id => id !== employeeId)
    );

  } else {

    setSelectedEmployees([
      ...selectedEmployees,
      employeeId
    ]);

  }

};
useEffect(() => {
  loadEmployees();
}, []);
  
useEffect(() => {
    loadTemplates();
}, []);

const loadTemplates = async () => {
    try {
        const data = await getTemplates();
        setTemplates(data);
    } catch (error) {
        console.error("Failed to load templates:", error);
    }
};

const handleTemplateSelect = async (templateId) => {
  try {
    const data = await getTemplate(templateId);

    setSelectedTemplate(templateId);
    setTemplate(data.template_name);
    setSubject(data.subject);
    setBody(data.content);

  } catch (error) {
    console.error(error);
  }
};
const handleSendCampaign = async () => {
  try {
    const campaignData = {
  campaign_name: template,
  email_subject: subject,
  email_template: body,
  difficulty: difficulty,
  status: "Draft",
  template_id: selectedTemplate,
};

    const campaign = await createCampaign(campaignData);

    await sendCampaign(campaign.campaign_id);

    alert("Campaign sent successfully!");

  } catch (error) {
    console.error(error);
    alert("Failed to send campaign.");
  }
};
 
const loadEmployees = async () => {
  try {
    const data = await getEmployees();
    setEmployees(data);
  } catch (error) {
    console.error("Failed to load employees:", error);
  }
}; 

  const suspiciousWords = [
    "Urgent",
    "Verify",
    "Password",
    "Immediately",
  ];

  const riskScore =
    difficulty === "Low"
      ? 25
      : difficulty === "Medium"
      ? 55
      : difficulty === "High"
      ? 82
      : 96;
const departments = [
  "All Departments",
  ...new Set(filteredEmployees.map((employee) => employee.department))
];
  return (
    <DashboardLayout>
      <div className="compose-page">

        <div className="page-header">
          <div>
            <h1>Compose Phishing Campaign</h1>
            <p>
              Create and launch simulated phishing campaigns for employee
              awareness.
            </p>
          </div>

          <button className="primary-btn">
            Preview Campaign
          </button>
        </div>

        <div className="compose-layout">

          {/* LEFT COLUMN */}

          <div className="left-column">
          {/* ===================== SENDER ===================== */}

<div className="card">

  <h3>Sender Information</h3>

  <div className="sender-card">

    <div className="sender-avatar">
      🛡️
    </div>

    <div className="sender-info">
      <h4>MIDHANI Security Team</h4>
      <p>security@midhani.in</p>
      <span className="sender-badge">
        Authorized Administrator
      </span>
    </div>

  </div>

</div>

{/* ===================== RECIPIENTS ===================== */}

<div className="card">

  <h3>Recipients</h3>

  <div className="grid-two">

    <div>

      <label>Department</label>

      <select
  value={department}
  onChange={(e) => setDepartment(e.target.value)}
>
  {departments.map((dept) => (
    <option key={dept} value={dept}>
      {dept}
    </option>
  ))}
</select>

    </div>

    <div>

      <label>Search Employee</label>

      <input
        type="text"
        placeholder="Search employee..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

    </div>

  </div>

  <div className="employee-list">

    {employees
  .filter(emp => {
    const matchesDepartment =
      department === "All Departments" ||
      emp.department === department;

    const matchesSearch =
      emp.name.toLowerCase().includes(search.toLowerCase());

    return matchesDepartment && matchesSearch;
  })
  .map(emp => (
    <label key={emp.id} className="employee-item">
      <input
    type="checkbox"
    checked={selectedEmployees.includes(emp.id)}
    onChange={() => handleEmployeeSelection(emp.id)}
/>
      <span>{emp.name}</span>
    </label>
))}

  </div>

</div>

{/* ===================== CAMPAIGN DETAILS ===================== */}

<div className="card">

  <h3>Campaign Details</h3>

  <label>Subject</label>

  <input
    type="text"
    placeholder="Enter campaign subject"
    value={subject}
    onChange={(e) => setSubject(e.target.value)}
  />

  <label className="section-label">
    Campaign Difficulty
  </label>

  <div className="difficulty-grid">

    {["Low", "Medium", "High", "Critical"].map((level) => (

      <div
        key={level}
        className={
          difficulty === level
            ? "difficulty-card active"
            : "difficulty-card"
        }
        onClick={() => setDifficulty(level)}
      >
        <h4>{level}</h4>
      </div>

    ))}

  </div>

  <label className="section-label">
    Email Template
  </label>

  <div className="template-grid">

    {templates.map((temp) => (

      <div
        key={temp.id}
        className={
          selectedTemplate === temp.id
            ? "template-card active"
            : "template-card"
        }
        onClick={() => handleTemplateSelect(temp.id)}
      >
        {temp.template_name}
      </div>

    ))}

  </div>

  <label>Email Body</label>

  <textarea
    rows="12"
    value={body}
    placeholder="Compose phishing email..."
    onChange={(e) => setBody(e.target.value)}
  />

  <div className="character-counter">
    {body.length} Characters
  </div>

</div>
{/* ===================== TRACKING ===================== */}

<div className="card">

  <h3>Tracking Options</h3>

  <div className="tracking-grid">

    <div className="tracking-card">
      <input type="checkbox" defaultChecked />
      <div>
        <h4>Click Tracking</h4>
        <p>Monitor every phishing link click.</p>
      </div>
    </div>

    <div className="tracking-card">
      <input type="checkbox" defaultChecked />
      <div>
        <h4>Credential Capture</h4>
        <p>Record submitted credentials safely.</p>
      </div>
    </div>

    <div className="tracking-card">
      <input type="checkbox" />
      <div>
        <h4>IP Address</h4>
        <p>Collect source IP information.</p>
      </div>
    </div>

    <div className="tracking-card">
      <input type="checkbox" />
      <div>
        <h4>Browser Details</h4>
        <p>Capture browser and operating system.</p>
      </div>
    </div>

  </div>

</div>

{/* ===================== ATTACHMENT ===================== */}

<div className="card">

  <h3>Attachment</h3>

  <div className="upload-box">

    <input
      type="file"
      onChange={(e) => setAttachment(e.target.files[0])}
    />

    {attachment ? (

      <div className="attachment-info">

        <strong>{attachment.name}</strong>

        <p>
          {(attachment.size / 1024).toFixed(2)} KB
        </p>

        <button
          className="secondary-btn"
          onClick={() => setAttachment(null)}
        >
          Remove
        </button>

      </div>

    ) : (

      <p>
        Drag & Drop or choose a file
      </p>

    )}

  </div>

</div>

{/* ===================== SCHEDULE ===================== */}

<div className="card">

  <h3>Schedule Campaign</h3>

  <div className="schedule-options">

    <label>

      <input
        type="radio"
        checked={schedule === "now"}
        onChange={() => setSchedule("now")}
      />

      Send Now

    </label>

    <label>

      <input
        type="radio"
        checked={schedule === "later"}
        onChange={() => setSchedule("later")}
      />

      Schedule Later

    </label>

  </div>

  {schedule === "later" && (

    <div className="grid-two">

      <div>

        <label>Date</label>

        <input type="date" />

      </div>

      <div>

        <label>Time</label>

        <input type="time" />

      </div>

    </div>

  )}

</div>

{/* ===================== BUTTONS ===================== */}

<div className="button-group">

  <button className="secondary-btn">
    Cancel
  </button>

  <button className="secondary-btn">
    Save Draft
  </button>

<button
    className="primary-btn"
    onClick={handleSendCampaign}
>
  
    Send Campaign
  </button>

</div>

</div>

{/* ===================== RIGHT PANEL ===================== */}

<div className="compose-right">
{/* ===================== LIVE PREVIEW ===================== */}

<div className="card">

  <h3>Live Email Preview</h3>

  <div className="email-preview">

    <p><strong>From:</strong> security@midhani.in</p>

    <p><strong>Subject:</strong> {subject || "Campaign Subject"}</p>

    <hr />

    <div className="preview-body">

      {body ? (
        <p style={{ whiteSpace: "pre-wrap" }}>{body}</p>
      ) : (
        <p className="placeholder-text">
          Email preview will appear here...
        </p>
      )}

    </div>

  </div>

</div>

{/* ===================== AI ANALYSIS ===================== */}

<div className="card">

  <h3>AI Campaign Analysis</h3>

  <div className="analysis-item">

    <span>Difficulty</span>

    <strong>{difficulty}</strong>

  </div>

  <div className="analysis-item">

    <span>Risk Score</span>

    <strong>{riskScore}%</strong>

  </div>

  <div className="analysis-item">

    <span>Template</span>

    <strong>{template}</strong>

  </div>

</div>

{/* ===================== RISK SCORE ===================== */}

<div className="card">

  <h3>Risk Score</h3>

  <div className="risk-bar">

    <div
      className="risk-fill"
      style={{ width: `${riskScore}%` }}
    ></div>

  </div>

  <h2>{riskScore}%</h2>

</div>

{/* ===================== SUSPICIOUS WORDS ===================== */}

<div className="card">

  <h3>Suspicious Keywords</h3>

  <div className="keyword-list">

    {suspiciousWords.map((word) => (

      <span
        key={word}
        className="keyword-chip"
      >
        {word}
      </span>

    ))}

  </div>

</div>

{/* ===================== TEMPLATE INFO ===================== */}

<div className="card">

  <h3>Template Information</h3>

  <p><strong>Selected:</strong> {template}</p>

  <p>
    This template is configured for phishing awareness
    simulations.
  </p>

</div>

</div>

{/* compose-layout */}

</div>

{/* compose-page */}

</div>

</DashboardLayout>

);

}

export default ComposeCampaign;