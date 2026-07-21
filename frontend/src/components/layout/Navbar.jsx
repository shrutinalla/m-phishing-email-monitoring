import { FaBell, FaUserCircle } from "react-icons/fa";
import "./Navbar.css";

function Navbar() {
  return (
    <header className="navbar">

      <div className="navbar-title">
        <h2>MIDHANI Phishing Email Monitoring System</h2>
      </div>

      <div className="navbar-right">

        <div className="notification">
          <FaBell />
        </div>

        <div className="profile">
          <FaUserCircle className="profile-icon" />

          <div>
            <h4>Administrator</h4>
            <span>Security Team</span>
          </div>
        </div>

      </div>

    </header>
  );
}

export default Navbar;