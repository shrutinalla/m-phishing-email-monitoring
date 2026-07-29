import { Routes, Route } from "react-router-dom";

import Login from "./pages/auth/Login";
import Dashboard from "./pages/dashboard/Dashboard";
import Employees from "./pages/employees/Employees";
import ComposeCampaign from "./pages/campaigns/ComposeCampaign";
import Reports from "./pages/reports/Reports";
import WarningPage from "./pages/warning/WarningPage";
import AwarenessPage from "./pages/awareness/AwarenessPage";

import ProtectedRoute from "./components/common/ProtectedRoute";
import routes from "./utils/routes";

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path={routes.LOGIN} element={<Login />} />
      <Route path={routes.WARNING} element={<WarningPage />} />

      {/* Protected Routes */}
      <Route
        path={routes.DASHBOARD}
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path={routes.EMPLOYEES}
        element={
          <ProtectedRoute>
            <Employees />
          </ProtectedRoute>
        }
      />

      <Route
        path={routes.CAMPAIGNS}
        element={
          <ProtectedRoute>
            <ComposeCampaign />
          </ProtectedRoute>
        }
      />

      <Route
        path={routes.REPORTS}
        element={
          <ProtectedRoute>
            <Reports />
          </ProtectedRoute>
        }
      />

      <Route
        path={routes.AWARENESS}
        element={
          <ProtectedRoute>
            <AwarenessPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;