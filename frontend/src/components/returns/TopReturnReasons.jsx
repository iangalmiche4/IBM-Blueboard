import { Column, Grid } from "@carbon/react";
import ReturnReasonCard from "./ReturnReasonCard";

/**
 * TopReturnReasons - Container component for displaying top return reasons
 * @param {Array} reasons - Array of return reason data
 * @param {Function} getReasonColor - Function to get color for reason tag
 * @param {number} maxItems - Maximum number of reasons to display (default: 5)
 */
function TopReturnReasons({ reasons, getReasonColor, maxItems = 5 }) {
  if (!reasons || reasons.length === 0) return null;

  const topReasons = reasons.slice(0, maxItems);

  return (
    <div className="top-return-reasons">
      <h4 className="reasons-section-title">Top Return Reasons</h4>
      <Grid>
        {topReasons.map((reason) => (
          <Column key={reason.reason} sm={4} md={4} lg={4}>
            <ReturnReasonCard reason={reason} getReasonColor={getReasonColor} />
          </Column>
        ))}
      </Grid>
    </div>
  );
}

export default TopReturnReasons;
