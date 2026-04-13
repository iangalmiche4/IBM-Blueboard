/**
 * ProgressBar - Reusable progress bar component
 *
 * @param {string} label - Text to display on the left
 * @param {string|number} value - Value to display on the right
 * @param {number} percentage - Fill percentage (0-100)
 * @param {string} color - Bar color
 * @param {number} height - Bar height in pixels (default: 8)
 * @param {string} size - Size variant: 'small', 'large' (default: normal)
 * @param {string} valueColor - Value text color
 */
function ProgressBar({
  label,
  value,
  percentage,
  color,
  height = 8,
  size,
  valueColor,
}) {
  const sizeClass = size ? `progress-bar--${size}` : "";

  return (
    <div className={`progress-bar ${sizeClass}`.trim()}>
      <div className="progress-bar__header">
        <span className="progress-bar__label">{label}</span>
        <span
          className="progress-bar__value"
          style={valueColor ? { color: valueColor } : undefined}
        >
          {value}
        </span>
      </div>
      <div
        className="progress-bar__track"
        style={
          height !== 8
            ? {
                height: `${height}px`,
                borderRadius: `${height / 2}px`,
              }
            : undefined
        }
      >
        <div
          className="progress-bar__fill"
          style={{
            width: `${Math.min(100, Math.max(0, percentage))}%`,
            ...(color && { backgroundColor: color }),
          }}
        />
      </div>
    </div>
  );
}

export default ProgressBar;
