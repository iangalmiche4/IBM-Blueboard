/**
 * SystemInfoItem - Reusable component for displaying system information items
 */
function SystemInfoItem({ label, value, icon }) {
  return (
    <div className="system-info-item">
      <div className="system-info-item__label">{label}</div>
      <div className="system-info-item__value">
        <span>{value}</span>
        {icon && <span>{icon}</span>}
      </div>
    </div>
  );
}

export default SystemInfoItem;
