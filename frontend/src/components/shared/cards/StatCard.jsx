import { Tile } from "@carbon/react";

function StatCard({ icon: Icon, title, value, subtitle, iconColor }) {
  return (
    <Tile className="stat-card">
      <div className="stat-card__header">
        {Icon && (
          <Icon
            size={24}
            className="stat-card__icon"
            style={iconColor ? { color: iconColor } : undefined}
          />
        )}
        <span className="stat-card__title">{title}</span>
      </div>
      <div className="stat-card__value">{value}</div>
      {subtitle && <div className="stat-card__subtitle">{subtitle}</div>}
    </Tile>
  );
}

export default StatCard;
