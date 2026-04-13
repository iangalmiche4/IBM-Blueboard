/**
 * InsightCard - Reusable insight card component with colored left border
 *
 * @param {string} title - Card title
 * @param {string} description - Card description text
 * @param {string} borderColor - Left border color
 * @param {string} titleColor - Title text color
 */
function InsightCard({ title, description, borderColor, titleColor }) {
  const finalTitleColor = titleColor || borderColor;

  return (
    <div
      className="insight-card"
      style={
        borderColor ? { borderLeft: `4px solid ${borderColor}` } : undefined
      }
    >
      <h5
        className="insight-card__title"
        style={finalTitleColor ? { color: finalTitleColor } : undefined}
      >
        {title}
      </h5>
      <p className="insight-card__description">{description}</p>
    </div>
  );
}

export default InsightCard;
