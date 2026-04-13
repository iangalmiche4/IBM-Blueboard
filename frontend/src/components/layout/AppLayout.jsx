import { Outlet, useNavigate } from "react-router-dom";
import { Asleep, Light, Settings } from "@carbon/icons-react";
import {
  Content,
  Header,
  HeaderContainer,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderMenuButton,
  HeaderName,
  SideNav,
  SideNavItems,
  Theme,
} from "@carbon/react";
import Navigation from "./Navigation";
import { useTheme } from "../../contexts/ThemeContext";

function AppLayout() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === "g10" ? "g100" : "g10");
  };

  return (
    <Theme theme="white">
      <HeaderContainer
        render={({ isSideNavExpanded, onClickSideNavExpand }) => (
          <>
            <Header aria-label="IBM Blueboard">
              <HeaderMenuButton
                aria-label={isSideNavExpanded ? "Close menu" : "Open menu"}
                onClick={onClickSideNavExpand}
                isActive={isSideNavExpanded}
              />
              <HeaderName
                href="/"
                prefix="IBM"
                onClick={(e) => {
                  e.preventDefault();
                  navigate("/");
                  if (isSideNavExpanded) {
                    onClickSideNavExpand();
                  }
                }}
              >
                Blueboard
              </HeaderName>
              <HeaderGlobalBar>
                <HeaderGlobalAction
                  aria-label={
                    theme === "g10"
                      ? "Switch to Dark Mode"
                      : "Switch to Light Mode"
                  }
                  tooltipAlignment="end"
                  onClick={toggleTheme}
                >
                  {theme === "g10" ? <Asleep size={20} /> : <Light size={20} />}
                </HeaderGlobalAction>
                <HeaderGlobalAction
                  aria-label="Settings"
                  tooltipAlignment="end"
                  onClick={() => navigate("/settings")}
                >
                  <Settings size={20} />
                </HeaderGlobalAction>
              </HeaderGlobalBar>
              <SideNav
                aria-label="Side navigation"
                expanded={isSideNavExpanded}
                isPersistent={false}
                onOverlayClick={onClickSideNavExpand}
                inert={isSideNavExpanded ? undefined : "true"}
              >
                <SideNavItems>
                  <Navigation
                    onNavigate={
                      isSideNavExpanded ? onClickSideNavExpand : undefined
                    }
                  />
                </SideNavItems>
              </SideNav>
            </Header>
            <Content className="app-content">
              <Outlet />
            </Content>
          </>
        )}
      />
    </Theme>
  );
}

export default AppLayout;
