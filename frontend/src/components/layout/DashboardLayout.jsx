import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import "./DashboardLayout.css";

function DashboardLayout({ children }) {
  return (
    <div className="layout">

      <Sidebar />

      <div className="main-section">

        <Navbar />

        <main className="content">
          {children}
        </main>

      </div>

    </div>
  );
}

export default DashboardLayout;