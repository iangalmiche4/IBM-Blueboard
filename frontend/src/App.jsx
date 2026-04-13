import {
  Navigate,
  Route,
  BrowserRouter as Router,
  Routes,
} from "react-router-dom";
import AppLayout from "./components/layout/AppLayout";
import { SettingsProvider } from "./contexts/SettingsContext";
import { ThemeProvider } from "./contexts/ThemeContext";

// Pages
import AdvancedAnalyticsPage from "./pages/AdvancedAnalyticsPage";
import CustomersPage from "./pages/CustomersPage";
import DashboardPage from "./pages/DashboardPage";
import InventoryPage from "./pages/InventoryPage";
import ProductsPage from "./pages/ProductsPage";
import PromotionsPage from "./pages/PromotionsPage";
import ReturnsPage from "./pages/ReturnsPage";
import SalesPage from "./pages/SalesPage";
import SatisfactionPage from "./pages/SatisfactionPage";
import SettingsPage from "./pages/SettingsPage";

// Styles
import "@carbon/styles/css/styles.css";
import "./styles/main.scss";

function App() {
  return (
    <SettingsProvider>
      <ThemeProvider>
        <Router
          future={{
            v7_startTransition: true,
            v7_relativeSplatPath: true,
          }}
        >
          <Routes>
            <Route element={<AppLayout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/sales" element={<SalesPage />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/customers" element={<CustomersPage />} />
              <Route path="/satisfaction" element={<SatisfactionPage />} />
              <Route path="/inventory" element={<InventoryPage />} />
              <Route path="/promotions" element={<PromotionsPage />} />
              <Route path="/returns" element={<ReturnsPage />} />
              <Route path="/analytics" element={<AdvancedAnalyticsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </Router>
      </ThemeProvider>
    </SettingsProvider>
  );
}

export default App;
