import { Tag } from "@carbon/react";
import { formatCurrency, formatPercentage } from "../../utils/formatters";

/**
 * ReturnReasonCard - Card component for displaying a single return reason
 * @param {Object} reason - Return reason data
 * @param {Function} getReasonColor - Function to get color for reason tag
 */
function ReturnReasonCard({ reason, getReasonColor }) {
  return (
    <div className="return-reason-card">
      <div className="reason-card-header">
        <Tag type={getReasonColor(reason.reason)} size="sm">
          {reason.reason}
        </Tag>
        <span className="reason-count">{reason.count}</span>
      </div>
      <div className="reason-card-stats">
        <div className="reason-stat">
          <strong>Percentage:</strong> {formatPercentage(reason.percentage)}
        </div>
        <div className="reason-stat">
          <strong>Total Refunded:</strong>{" "}
          {formatCurrency(reason.total_refund_amount)}
        </div>
      </div>
    </div>
  );
}

export default ReturnReasonCard;
