import { useEffect, useRef, useState } from "react";
import { Responsive as ResponsiveGridLayout } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";

/**
 * DraggableDashboardGrid - A responsive draggable grid layout
 * Persists layout to localStorage
 * Adapts to screen size with breakpoints
 */
function DraggableDashboardGrid({ children, onLayoutChange }) {
  const STORAGE_KEY = "ibm-blueboard-dashboard-layout";
  const containerRef = useRef(null);
  const [width, setWidth] = useState(1200);

  // Default layout configuration for different breakpoints
  const defaultLayouts = {
    lg: [
      {
        i: "kpi-revenue",
        x: 0,
        y: 0,
        w: 3,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "kpi-sales",
        x: 3,
        y: 0,
        w: 3,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "kpi-satisfaction",
        x: 6,
        y: 2,
        w: 3,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "kpi-basket",
        x: 9,
        y: 2,
        w: 3,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "chart-sales-trends",
        x: 0,
        y: 2,
        w: 6,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "chart-channels",
        x: 6,
        y: 0,
        w: 6,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "chart-regions",
        x: 0,
        y: 4,
        w: 3,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      {
        i: "kpi-stats",
        x: 3,
        y: 4,
        w: 3,
        h: 2,
        minW: 2,
        minH: 2,
        maxW: 6,
        maxH: 2,
      },
      { i: "promotion_roi", x: 6, y: 4, w: 6, h: 2, minW: 3, minH: 2 },
    ],
    md: [
      { i: "kpi-revenue", x: 0, y: 0, w: 3, h: 2, minW: 2, minH: 2 },
      { i: "kpi-sales", x: 3, y: 0, w: 3, h: 2, minW: 2, minH: 2 },
      { i: "kpi-satisfaction", x: 0, y: 2, w: 3, h: 2, minW: 2, minH: 2 },
      { i: "kpi-basket", x: 3, y: 2, w: 3, h: 2, minW: 2, minH: 2 },
      { i: "chart-sales-trends", x: 0, y: 4, w: 6, h: 2, minW: 2, minH: 2 },
      { i: "chart-channels", x: 0, y: 6, w: 6, h: 2, minW: 2, minH: 2 },
      { i: "chart-regions", x: 0, y: 8, w: 6, h: 2, minW: 2, minH: 2 },
      { i: "kpi-stats", x: 0, y: 10, w: 3, h: 2, minW: 2, minH: 2 },
      { i: "promotion_roi", x: 0, y: 12, w: 6, h: 2 },
    ],
    sm: [
      { i: "kpi-revenue", x: 0, y: 0, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "kpi-sales", x: 0, y: 2, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "kpi-satisfaction", x: 0, y: 4, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "kpi-basket", x: 0, y: 6, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "chart-sales-trends", x: 0, y: 8, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "chart-channels", x: 0, y: 10, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "chart-regions", x: 0, y: 12, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "kpi-stats", x: 0, y: 14, w: 2, h: 2, minW: 2, minH: 2 },
      { i: "promotion_roi", x: 0, y: 16, w: 2, h: 2, minW: 2, minH: 2 },
    ],
  };

  // Load layouts from localStorage or use default
  const [layouts, setLayouts] = useState(() => {
    const savedLayouts = localStorage.getItem(STORAGE_KEY);
    return savedLayouts ? JSON.parse(savedLayouts) : defaultLayouts;
  });

  // Save layouts to localStorage when they change
  const handleLayoutChange = (currentLayout, allLayouts) => {
    setLayouts(allLayouts);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    if (onLayoutChange) {
      onLayoutChange(currentLayout, allLayouts);
    }
  };

  // Reset layouts to default
  const resetLayout = () => {
    setLayouts(defaultLayouts);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultLayouts));
  };

  // Measure container width on mount and resize
  useEffect(() => {
    const measureWidth = () => {
      if (containerRef.current) {
        setWidth(containerRef.current.offsetWidth);
      }
    };

    measureWidth();
    window.addEventListener("resize", measureWidth);

    return () => {
      window.removeEventListener("resize", measureWidth);
    };
  }, []);

  // Expose reset function globally for easy access
  useEffect(() => {
    window.resetDashboardLayout = resetLayout;
    return () => {
      delete window.resetDashboardLayout;
    };
  }, []);

  return (
    <div className="draggable-dashboard-container" ref={containerRef}>
      <ResponsiveGridLayout
        className="draggable-dashboard-grid"
        layouts={layouts}
        breakpoints={{ lg: 1200, md: 996, sm: 768 }}
        cols={{ lg: 12, md: 6, sm: 2 }}
        rowHeight={150}
        width={width}
        onLayoutChange={handleLayoutChange}
        draggableHandle=".drag-handle"
        compactType="vertical"
        preventCollision={false}
        margin={[16, 16]}
        containerPadding={[0, 0]}
        isDraggable={true}
        isResizable={true}
        resizeHandles={["se"]}
      >
        {children}
      </ResponsiveGridLayout>
    </div>
  );
}

export default DraggableDashboardGrid;
