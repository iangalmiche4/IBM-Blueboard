import { Tile } from "@carbon/react";
import { BarChart } from "@mui/x-charts/BarChart";
import PropTypes from "prop-types";
import { CHART_COLORS } from "../../constants/chartColors";

/**
 * MUI Bar Chart Component
 * Displays data in a bar chart format
 * Note: Should be wrapped in WidgetContainer for drag & drop functionality
 */
function MuiBarChart({
  title,
  data,
  height = 300,
  xAxisKey = "label",
  yAxisKey = "value",
  horizontal = false,
  yAxisFormatter = (val) => val?.toString(),
  valueFormatter = (val) => val?.toString(),
}) {
  // Extract labels and values
  const labels = data?.map(
    (item) => item[xAxisKey] || item.label || item.group || "",
  ) || [];

  const values = data?.map((item) => item[yAxisKey] || item.value || 0) || [];

  const isEmpty = !data || data.length === 0;
  const tileClassName = isEmpty
    ? "mui-chart-tile mui-chart-tile--empty"
    : "mui-chart-tile";

  return (
    <Tile className={tileClassName}>
      {title && <h3 className="mui-chart-title">{title}</h3>}
      {!isEmpty ? (
        <div className="mui-chart-body">
          <BarChart
            xAxis={[
              {
                scaleType: "band",
                data: labels,
                tickLabelStyle: {
                  angle: labels.length > 5 ? -45 : 0,
                  textAnchor: labels.length > 5 ? "end" : "middle",
                  fontSize: 11,
                },
              },
            ]}
            yAxis={[
              {
                tickLabelStyle: {
                  fontSize: 11,
                },
                valueFormatter: yAxisFormatter,
              },
            ]}
            series={[
              {
                data: values,
                color: CHART_COLORS.bar,
                valueFormatter: valueFormatter,
              },
            ]}
            height={height}
            layout={horizontal ? "horizontal" : "vertical"}
            margin={{
              top: 10,
              right: 10,
              bottom: labels.length > 5 ? 60 : 30,
              left: 50,
            }}
            slotProps={{
              legend: {
                hidden: true,
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

MuiBarChart.propTypes = {
  title: PropTypes.string,
  data: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      group: PropTypes.string,
      value: PropTypes.number,
    }),
  ).isRequired,
  height: PropTypes.number,
  xAxisKey: PropTypes.string,
  yAxisKey: PropTypes.string,
  horizontal: PropTypes.bool,
  yAxisFormatter: PropTypes.func,
  valueFormatter: PropTypes.func,
};

export default MuiBarChart;
