import { useLocation, useNavigate } from "react-router-dom";
import {
  Analytics,
  Catalog,
  ChartLine,
  Dashboard,
  FaceAdd,
  InventoryManagement,
  Purchase,
  Renew,
  Settings,
  ShoppingCart,
} from "@carbon/icons-react";
import { SideNavLink } from "@carbon/react";

const navigationItems = [
  {
    id: "dashboard",
    label: "Dashboard",
    href: "/",
    icon: Dashboard,
  },
  {
    id: "sales",
    label: "Sales Analytics",
    href: "/sales",
    icon: ChartLine,
  },
  {
    id: "products",
    label: "Products",
    href: "/products",
    icon: Catalog,
  },
  {
    id: "customers",
    label: "Customers",
    href: "/customers",
    icon: ShoppingCart,
  },
  {
    id: "satisfaction",
    label: "Satisfaction",
    href: "/satisfaction",
    icon: FaceAdd,
  },
  {
    id: "inventory",
    label: "Inventory",
    href: "/inventory",
    icon: InventoryManagement,
  },
  {
    id: "promotions",
    label: "Promotions",
    href: "/promotions",
    icon: Purchase,
  },
  {
    id: "returns",
    label: "Returns",
    href: "/returns",
    icon: Renew,
  },
  {
    id: "analytics",
    label: "Advanced Analytics",
    href: "/analytics",
    icon: Analytics,
  },
  {
    id: "settings",
    label: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

function Navigation({ onNavigate }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (href) => {
    // Navigate immediately for instant response
    navigate(href);
    // Close the side nav in parallel if callback is provided
    if (onNavigate) {
      onNavigate();
    }
  };

  return (
    <>
      {navigationItems.map((item) => (
        <SideNavLink
          key={item.id}
          renderIcon={item.icon}
          href={item.href}
          isActive={location.pathname === item.href}
          onClick={(e) => {
            e.preventDefault();
            handleNavigation(item.href);
          }}
        >
          {item.label}
        </SideNavLink>
      ))}
    </>
  );
}

export default Navigation;
