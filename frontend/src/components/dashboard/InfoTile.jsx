import { Tile } from "@carbon/react";

function InfoTile({ title, icon: Icon, children, className = "" }) {
  return (
    <Tile className={`zone-tile ${className}`}>
      <div className="tile-header">
        <h3>{title}</h3>
        {Icon && <Icon size={24} className="info-tile__icon" />}
      </div>
      <div className="info-tile__content">{children}</div>
    </Tile>
  );
}

export default InfoTile;
