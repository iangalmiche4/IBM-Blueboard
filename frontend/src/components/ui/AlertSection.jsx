import PropTypes from "prop-types";
import { WarningAlt } from "@carbon/icons-react";
import { Grid } from "@carbon/react";

/**
 * AlertSection Component
 * Generic alert section that displays warnings with items in grid format using AlertCard
 *
 * @param {string} title - Alert title
 * @param {string} description - Alert description
 * @param {Array} items - Array of items to display
 * @param {Function} renderItem - Function to render each item as AlertCard
 */
function AlertSection({ title, description, items = [], renderItem }) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div className="alert-section">
      {/* Title */}
      <div className="alert-header">
        <WarningAlt size={20} className="alert-icon" />
        <h4 className="alert-title">{title}</h4>
      </div>

      {/* Description */}
      <p className="alert-description">{description}</p>

      {/* Content - Always Grid */}
      <Grid>
        {items.map((item, index) =>
          renderItem ? renderItem(item, index) : null,
        )}
      </Grid>
    </div>
  );
}

AlertSection.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  items: PropTypes.array.isRequired,
  renderItem: PropTypes.func.isRequired,
};

export default AlertSection;
