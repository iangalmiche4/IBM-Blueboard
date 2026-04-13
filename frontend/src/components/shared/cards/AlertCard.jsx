import PropTypes from "prop-types";
import { Column } from "@carbon/react";

/**
 * AlertCard Component
 * Generic card component for displaying data in alert sections
 *
 * @param {string} title - Card title
 * @param {Array} fields - Array of field objects with { label, value }
 * @param {number} sm - Small breakpoint columns (default: 4)
 * @param {number} md - Medium breakpoint columns (default: 4)
 * @param {number} lg - Large breakpoint columns (default: 4)
 */
function AlertCard({ title, fields = [], sm = 4, md = 4, lg = 4 }) {
  return (
    <Column sm={sm} md={md} lg={lg}>
      <div className="alert-card">
        {/* Card Title */}
        <h5 className="alert-card-title">{title}</h5>

        {/* Card Fields */}
        <div className="alert-card-content">
          {fields.map((field, index) => (
            <p
              key={field.label || `field-${index}`}
              className="alert-card-field"
            >
              <strong>↳ {field.label}:</strong> <span>{field.value}</span>
            </p>
          ))}
        </div>
      </div>
    </Column>
  );
}

AlertCard.propTypes = {
  title: PropTypes.string.isRequired,
  fields: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      value: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number,
        PropTypes.node,
      ]).isRequired,
    }),
  ).isRequired,
  sm: PropTypes.number,
  md: PropTypes.number,
  lg: PropTypes.number,
};

export default AlertCard;
