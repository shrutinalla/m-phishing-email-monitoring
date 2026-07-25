import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import "./Employees.css";

import {
  getEmployees,
  addEmployee,
  deleteEmployee,
  searchEmployees,
} from "../../services/employeeService";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [showModal, setShowModal] = useState(false);

  const [search, setSearch] = useState("");

  const [form, setForm] = useState({
    name: "",
    email: "",
    department: "",
  });

  const loadEmployees = async () => {
    try {
      const data = await getEmployees();
      setEmployees(data);
    } catch (err) {
      console.log(err);
      alert("Failed to load employees");
    }
  };

  useEffect(() => {
    loadEmployees();
  }, []);

  const handleInput = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleAdd = async () => {
    if (
      !form.name ||
      !form.email ||
      !form.department
    ) {
      alert("Fill all fields");
      return;
    }

    try {

    await addEmployee(form);

    setForm({
        name: "",
        email: "",
        department: "",
    });

    setShowModal(false);

    await loadEmployees();

    alert("Employee Added Successfully");

} catch (err) {

    console.log(err);

    alert("Unable to add employee");

}
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete Employee?")) return;

    try {
      await deleteEmployee(id);

      loadEmployees();
    } catch (err) {
      console.log(err);
      alert("Delete Failed");
    }
  };

  const handleSearch = async (value) => {
    setSearch(value);

    if (value.trim() === "") {
      loadEmployees();
      return;
    }

    try {
      const data = await searchEmployees(value);

      setEmployees(data);
    } catch (err) {
      console.log(err);
    }
  };
    return (
    <DashboardLayout>
      <div className="employee-page">

        <div className="employee-header">

          <h1>Employees</h1>

          <div className="top-actions">

            <input
              className="search-box"
              type="text"
              placeholder="Search employee..."
              value={search}
              onChange={(e) => handleSearch(e.target.value)}
            />

            <button
              className="add-btn"
              onClick={() => setShowModal(true)}
            >
              + Add Employee
            </button>

          </div>

        </div>

        <div className="employee-table">

          <table>

            <thead>

              <tr>

                <th>ID</th>

                <th>Name</th>

                <th>Email</th>

                <th>Department</th>

                <th>Risk</th>

                <th>Action</th>

              </tr>

            </thead>

            <tbody>

              {employees.length === 0 ? (

                <tr>

                  <td
                    colSpan="6"
                    style={{
                      textAlign: "center",
                      padding: "30px",
                    }}
                  >
                    No Employees Found
                  </td>

                </tr>

              ) : (

                employees.map((employee) => (

                  <tr key={employee.id}>

                    <td>{employee.id}</td>

                    <td>{employee.name}</td>

                    <td>{employee.email}</td>

                    <td>{employee.department}</td>

                    <td>{employee.risk_level}</td>

                    <td>

                      <button
                        className="delete-btn"
                        onClick={() =>
                          handleDelete(employee.id)
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

          <div className="modal">

            <div className="modal-content">

              <h2>Add Employee</h2>

              <input
                name="name"
                placeholder="Employee Name"
                value={form.name}
                onChange={handleInput}
              />

              <input
                name="email"
                placeholder="Employee Email"
                value={form.email}
                onChange={handleInput}
              />

              <input
                name="department"
                placeholder="Department"
                value={form.department}
                onChange={handleInput}
              />

              <div className="modal-buttons">

                <button
                  className="cancel-btn"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>

                <button
                  className="save-btn"
                  onClick={handleAdd}
                >
                  Save
                </button>

              </div>

            </div>

          </div>

        )}

      </div>
    </DashboardLayout>
  );
}

export default Employees;