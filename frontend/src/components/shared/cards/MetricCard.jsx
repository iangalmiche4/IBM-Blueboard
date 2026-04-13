import { Tile } from "@carbon/react";
import { formatCurrency } from "../../../utils/formatters";

/**
 * MetricCard - Reusable card component for displaying metrics with colored items
 * @param {string} title - Card title
 * @param {Array} data - Array of items with { group, value } structure
 * @param {string} emptyMessage - Message to display when no data (default: "No data available")
 * @param {Array} colors - Array of colors to alternate (default: ['#0f62fe', '#4589ff'])
 * @param {Function} formatValue - Function to format the value (default: formatCurrency)
 */
function MetricCard({
  title,
  data = [],
  emptyMessage = "No data available",
  colors = ["#0f62fe", "#4589ff"],
  formatValue = formatCurrency,
}) {
  return (
    <Tile className="metric-card">
      <h3 className="metric-card__title">{title}</h3>
      {data.length > 0 ? (
        <div className="metric-card__list">
          {data.map((item, index) => {
            const color = colors[index % colors.length];
            return (
              <div
                key={index}
                className="metric-card__item"
                style={{ borderLeft: `4px solid ${color}` }}
              >
                <span className="metric-card__label">{item.group}</span>
                <span className="metric-card__value" style={{ color: color }}>
                  {formatValue(item.value)}
                </span>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="metric-card__empty">{emptyMessage}</p>
      )}
    </Tile>
  );
}

export default MetricCard;
