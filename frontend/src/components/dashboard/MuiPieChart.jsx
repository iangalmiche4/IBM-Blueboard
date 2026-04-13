import { PieChart } from "@mui/x-charts/PieChart";
import PropTypes from "prop-types";
import { Tile } from "@carbon/react";
import { CHART_COLORS } from "../../constants/chartColors";
import { useTheme } from "../../contexts/ThemeContext";

/**
 * MUI Pie Chart Component
 * Displays data in a pie/donut chart format with percentages
 * Note: Should be wrapped in WidgetContainer for drag & drop functionality
 */
function MuiPieChart({
  title,
  data,
  height = 300,
  innerRadius = 0,
  outerRadius = 100,
}) {
  const { theme } = useTheme();

  // Transform data to MUI format with percentages and colors
  const total = data.reduce((sum, item) => sum + (item.value || 0), 0);
  const chartData = data.map((item, index) => ({
    id: index,
    value: item.value || 0,
    label: item.label || item.group || `Item ${index + 1}`,
    percentage: total > 0 ? ((item.value / total) * 100).toFixed(1) : 0,
    color: CHART_COLORS.primary[index % CHART_COLORS.primary.length],
  }));

  const isEmpty = !data || data.length === 0;
  const tileClassName = isEmpty
    ? "mui-chart-tile mui-chart-tile--empty"
    : "mui-chart-tile";

  return (
    <Tile className={tileClassName}>
      {title && <h3 className="mui-chart-title">{title}</h3>}
      {!isEmpty ? (
        <div className="mui-chart-body">
          <PieChart
            series={[
              {
                data: chartData,
                innerRadius,
                outerRadius,
                paddingAngle: 2,
                cornerRadius: 4,
                highlightScope: { faded: "global", highlighted: "item" },
                faded: {
                  innerRadius: 30,
                  additionalRadius: -10,
                  color: "gray",
                },
              },
            ]}
            colors={CHART_COLORS.primary}
            height={height}
            slotProps={{
              legend: { hidden: true },
            }}
            tooltip={{
              trigger: "item",
            }}
            sx={{
              "& .MuiPieArc-root": {
                stroke: theme === "g100" ? "transparent" : "#ffffff",
                strokeWidth: theme === "g100" ? 0 : 1,
              },
            }}
          />
        </div>
      ) : (
        <p className="mui-chart-empty">No data available</p>
      )}
    </Tile>
  );
}

MuiPieChart.propTypes = {
  title: PropTypes.string,
  data: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      group: PropTypes.string,
      value: PropTypes.number.isRequired,
    }),
  ).isRequired,
  height: PropTypes.number,
  innerRadius: PropTypes.number,
  outerRadius: PropTypes.number,
};

export default MuiPieChart;
