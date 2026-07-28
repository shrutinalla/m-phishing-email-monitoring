import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import api from "../../services/api";
import "./Templates.css";

function Templates() {
  const [templates, setTemplates] = useState([]);
  const [filteredTemplates, setFilteredTemplates] = useState([]);

  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [showModal, setShowModal] = useState(false);

  const [editingId, setEditingId] = useState(null);

  const [previewData, setPreviewData] = useState(null);

  const [showPreview, setShowPreview] = useState(false);

  const [formData, setFormData] = useState({
    template_name: "",
    subject: "",
    content: "",
  });

  useEffect(() => {
    loadTemplates();
  }, []);

  useEffect(() => {
    if (search.trim() === "") {
      setFilteredTemplates(templates);
    } else {
      setFilteredTemplates(
        templates.filter(
          (template) =>
            template.template_name
              .toLowerCase()
              .includes(search.toLowerCase()) ||
            template.subject
              .toLowerCase()
              .includes(search.toLowerCase())
        )
      );
    }
  }, [search, templates]);

  const loadTemplates = async () => {
    try {
      setLoading(true);

      const res = await api.get("/templates");

      setTemplates(res.data);

      setFilteredTemplates(res.data);

      setError("");
    } catch (err) {
      console.error(err);

      setError("Failed to load templates.");
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setEditingId(null);

    setFormData({
      template_name: "",
      subject: "",
      content: "",
    });
  };

  const openCreate = () => {
    resetForm();

    setShowModal(true);
  };

  const openEdit = (template) => {
    setEditingId(template.id);

    setFormData({
      template_name: template.template_name,
      subject: template.subject,
      content: template.content,
    });

    setShowModal(true);
  };

  const saveTemplate = async () => {
    try {
      if (
        !formData.template_name ||
        !formData.subject ||
        !formData.content
      ) {
        alert("Fill all fields.");

        return;
      }

      if (editingId) {
        await api.put(
          `/templates/${editingId}`,
          formData
        );
      } else {
        await api.post(
          "/templates",
          formData
        );
      }

      setShowModal(false);

      resetForm();

      loadTemplates();
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
          "Operation failed."
      );
    }
  };

  const deleteTemplate = async (id) => {
    if (
      !window.confirm(
        "Delete this template?"
      )
    )
      return;

    try {
      await api.delete(`/templates/${id}`);

      loadTemplates();
    } catch (err) {
      console.error(err);

      alert("Delete failed.");
    }
  };

  const previewTemplate = async (id) => {
    try {
      const res = await api.get(
        `/templates/${id}/preview`
      );

      setPreviewData(res.data);

      setShowPreview(true);
    } catch (err) {
      console.error(err);
    }
  };

  

  if (loading) {
    return (
      <DashboardLayout>
        <div className="templates-page">
          <h2>Loading Templates...</h2>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="templates-page">
          <h2>{error}</h2>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="templates-page">

        <div className="templates-header">

          <div>

            <h1>Email Templates</h1>

            <p>
              Manage phishing email templates.
            </p>

          </div>

          <button
            className="create-btn"
            onClick={openCreate}
          >
            + New Template
          </button>

        </div>

        <div className="search-card">

          <input
            type="text"
            placeholder="Search template..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />

        </div>

        <div className="table-card">

          <table className="template-table">

            <thead>

              <tr>

                <th>Name</th>

                <th>Subject</th>

                <th>Campaigns</th>

                <th>Preview</th>

                <th>Actions</th>

              </tr>

            </thead>

            <tbody>
                              {filteredTemplates.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ textAlign: "center" }}>
                    No templates found.
                  </td>
                </tr>
              ) : (
                filteredTemplates.map((template) => (
                  <tr key={template.id}>
                    <td>{template.template_name}</td>

                    <td>{template.subject}</td>

                    <td>
                      <button
  className="count-btn"
  onClick={() =>
    alert(
      `${template.campaign_count} campaign(s) are using this template.`
    )
  }
>
  {template.campaign_count}
</button>
                    </td>

                    <td>
                      <button
                        className="preview-btn"
                        onClick={() =>
                          previewTemplate(template.id)
                        }
                      >
                        Preview
                      </button>
                    </td>

                    <td>
                      <button
                        className="edit-btn"
                        onClick={() => openEdit(template)}
                      >
                        Edit
                      </button>

                      <button
                        className="delete-btn"
                        onClick={() =>
                          deleteTemplate(template.id)
                        }
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>

          </table>

        </div>

        {showModal && (
          <div className="modal-overlay">
            <div className="modal">

              <h2>
                {editingId
                  ? "Edit Template"
                  : "Create Template"}
              </h2>

              <input
                type="text"
                placeholder="Template Name"
                value={formData.template_name}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    template_name: e.target.value,
                  })
                }
              />

              <input
                type="text"
                placeholder="Subject"
                value={formData.subject}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    subject: e.target.value,
                  })
                }
              />

              <textarea
                rows="10"
                placeholder="Email Content"
                value={formData.content}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    content: e.target.value,
                  })
                }
              />

              <div className="modal-buttons">

                <button
                  className="save-btn"
                  onClick={saveTemplate}
                >
                  Save
                </button>

                <button
                  className="cancel-btn"
                  onClick={() => {
                    setShowModal(false);
                    resetForm();
                  }}
                >
                  Cancel
                </button>

              </div>

            </div>
          </div>
        )}

        {showPreview && previewData && (
          <div className="modal-overlay">
            <div className="preview-modal">

              <h2>{previewData.template_name}</h2>

              <h4>{previewData.subject}</h4>

              <hr />

              <div className="preview-content">
                {previewData.content}
              </div>

              <button
                className="cancel-btn"
                onClick={() => {
                  setShowPreview(false);
                  setPreviewData(null);
                }}
              >
                Close
              </button>

            </div>
          </div>
        )}

      </div>
    </DashboardLayout>
  );
}

export default Templates;