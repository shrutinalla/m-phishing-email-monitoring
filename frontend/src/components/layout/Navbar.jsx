import { FaBell, FaUserCircle, FaSignOutAlt } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./Navbar.css";

function Navbar() {

    const navigate = useNavigate();
    const { logout } = useAuth();

    const username = localStorage.getItem("username") || "Administrator";

    const handleLogout = () => {
        logout();
        localStorage.removeItem("username");
        navigate("/");
    };

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

                        <h4>{username}</h4>

                        <span>Security Administrator</span>

                    </div>

                </div>

                <button
                    className="logout-btn"
                    onClick={handleLogout}
                >
                    <FaSignOutAlt />
                </button>

            </div>

        </header>
    );
}

export default Navbar;