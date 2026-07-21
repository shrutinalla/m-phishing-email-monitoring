import { NavLink } from "react-router-dom";
import {
  FaTachometerAlt,
  FaUsers,
  FaEnvelope,
  FaChartBar,
  FaShieldAlt,
  FaSignOutAlt,
} from "react-icons/fa";

import routes from "../../utils/routes";

import "./Sidebar.css";

const menuItems = [
  {
    name: "Dashboard",
    path: routes.DASHBOARD,
    icon: <FaTachometerAlt />,
  },
  {
    name: "Employees",
    path: routes.EMPLOYEES,
    icon: <FaUsers />,
  },
  {
    name: "Campaigns",
    path: routes.CAMPAIGNS,
    icon: <FaEnvelope />,
  },
  {
    name: "Reports",
    path: routes.REPORTS,
    icon: <FaChartBar />,
  },
  {
    name: "Awareness",
    path: routes.AWARENESS,
    icon: <FaShieldAlt />,
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <FaShieldAlt className="logo-icon" />
        <div>
          <h2>MIDHANI</h2>
          <span>Security Portal</span>
        </div>
      </div>

      <nav>
        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "menu-item active" : "menu-item"
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="logout">
        <FaSignOutAlt />
        <span>Logout</span>
      </div>
    </aside>
  );
}

export default Sidebar;