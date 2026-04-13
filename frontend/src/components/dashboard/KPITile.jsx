import { ArrowDown, ArrowUp } from "@carbon/icons-react";
import { Tile } from "@carbon/react";

function KPITile({
  title,
  subtitle,
  value,
  icon: Icon,
  change,
  changeLabel = "vs last month",
}) {
  const renderChangeIndicator = () => {
    if (!change && change !== 0) return null;

    if (change > 0) {
      return (
        <span className="tile-change positive">
          <ArrowUp size={16} />
          {change.toFixed(1)}% {changeLabel}
        </span>
      );
    } else if (change < 0) {
      return (
        <span className="tile-change negative">
          <ArrowDown size={16} />
          {Math.abs(change).toFixed(1)}% {changeLabel}
        </span>
      );
    }
    return <span className="tile-change neutral">No change {changeLabel}</span>;
  };

  return (
    <Tile className="zone-tile">
      <div className="tile-header">
        <h3>{title}</h3>
        {subtitle && <p className="tile-subtitle">{subtitle}</p>}
        {Icon && <Icon size={24} />}
      </div>
      <div className="tile-value">{value ?? "-"}</div>
      {renderChangeIndicator()}
    </Tile>
  );
}

export default KPITile;
