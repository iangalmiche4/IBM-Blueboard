import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Tile } from "@carbon/react";
import { useTheme } from "../../contexts/ThemeContext";

function RechartsWidget({ title, data, emptyMessage = "No data available" }) {
  const { theme } = useTheme();

  // Theme colors
  const isDark = theme === "g100";
  const colors = {
    text: isDark ? "#f4f4f4" : "#161616",
    grid: isDark ? "#393939" : "#e0e0e0",
    line: "#0f62fe", // IBM Blue
  };

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="recharts-widget__tooltip">
          <p className="recharts-widget__tooltip-date">
            {new Date(payload[0].payload.date).toLocaleDateString("fr-FR", {
              month: "short",
              year: "numeric",
            })}
          </p>
          <p className="recharts-widget__tooltip-value">
            {payload[0].value.toLocaleString("fr-FR", {
              style: "currency",
              currency: "EUR",
              minimumFractionDigits: 0,
              maximumFractionDigits: 0,
            })}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Tile className="zone-tile recharts-widget">
      {title && (
        <div className="recharts-widget__header">
          <h3>{title}</h3>
        </div>
      )}
      {data && data.length > 0 ? (
        <div className="recharts-widget__chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
              <XAxis
                dataKey="date"
                stroke={colors.text}
                tick={{ fill: colors.text, fontSize: 12 }}
                tickFormatter={(value) => {
                  const date = new Date(value);
                  return date.toLocaleDateString("fr-FR", { month: "short" });
                }}
              />
              <YAxis
                stroke={colors.text}
                tick={{ fill: colors.text, fontSize: 12 }}
                tickFormatter={(value) => `${(value / 1000).toFixed(0)}k€`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="value"
                stroke={colors.line}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 8 }}
                fill="transparent"
                fillOpacity={0}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <p className="recharts-widget__empty">{emptyMessage}</p>
      )}
    </Tile>
  );
}

export default RechartsWidget;
