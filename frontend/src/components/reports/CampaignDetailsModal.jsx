import "./CampaignDetailsModal.css";

function CampaignDetailsModal({ open, onClose, campaignData }) {
  if (!open || !campaignData) return null;

  const { campaign, employees } = campaignData;

  return (
    <div className="modal-overlay">
      <div className="campaign-modal">

        <div className="modal-header">
          <h2>Campaign Details</h2>

          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="campaign-info">

          <div className="info-item">
            <strong>Campaign</strong>
            <span>{campaign.campaign_name}</span>
          </div>

          <div className="info-item">
            <strong>Subject</strong>
            <span>{campaign.email_subject}</span>
          </div>

          <div className="info-item">
            <strong>Difficulty</strong>
            <span>{campaign.difficulty}</span>
          </div>

          <div className="info-item">
            <strong>Status</strong>
            <span>{campaign.status}</span>
          </div>

          <div className="info-item">
            <strong>Recipients</strong>
            <span>{campaign.total_recipients}</span>
          </div>

          <div className="info-item">
            <strong>Emails Sent</strong>
            <span>{campaign.emails_sent}</span>
          </div>

          <div className="info-item">
            <strong>Emails Failed</strong>
            <span>{campaign.emails_failed}</span>
          </div>

          <div className="info-item">
            <strong>Emails Clicked</strong>
            <span>{campaign.emails_clicked}</span>
          </div>

          <div className="info-item">
            <strong>Click Rate</strong>
            <span>{campaign.click_rate}%</span>
          </div>

          <div className="info-item">
            <strong>Attachment</strong>
            <span>{campaign.attachment_name || "None"}</span>
          </div>

        </div>

        <h3 className="employee-heading">
          Employee Click Activity
        </h3>

        <div className="employee-table-wrapper">

          <table className="employee-table">

            <thead>

              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Clicked Time</th>
                <th>IP Address</th>
                <th>Browser</th>
              </tr>

            </thead>

            <tbody>

              {employees.length === 0 ? (

                <tr>

                  <td
                    colSpan="5"
                    style={{ textAlign: "center" }}
                  >
                    No employee has clicked this campaign.
                  </td>

                </tr>

              ) : (

                employees.map((employee) => (

                  <tr key={employee.employee_id}>

                    <td>{employee.employee_name}</td>

                    <td>{employee.email}</td>

                    <td>
                      {new Date(
                        employee.clicked_time
                      ).toLocaleString()}
                    </td>

                    <td>{employee.ip_address}</td>

                    <td>{employee.user_agent}</td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>
    </div>
  );
}

export default CampaignDetailsModal;