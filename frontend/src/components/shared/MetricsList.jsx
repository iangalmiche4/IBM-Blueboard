function MetricsList({ items, formatValue, colors = ["#0f62fe", "#4589ff"] }) {
  return (
    <div className="metrics-list">
      {items.map((item, index) => {
        const color = colors[index % colors.length];
        return (
          <div
            key={index}
            className="metrics-list__item"
            style={{ borderLeft: `4px solid ${color}` }}
          >
            <span className="metrics-list__label">{item.label}</span>
            <span className="metrics-list__value" style={{ color: color }}>
              {formatValue ? formatValue(item.value) : item.value}
            </span>
          </div>
        );
      })}
    </div>
  );
}

export default MetricsList;
