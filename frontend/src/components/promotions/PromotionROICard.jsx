import { Tag } from "@carbon/react";
import { formatCurrency } from "../../utils/formatters";

/**
 * PromotionROICard - Individual promotion ROI card
 * Displays ranking, promo code, usage stats, and revenue metrics
 */
function PromotionROICard({ promotion, rank }) {
  return (
    <div className="promotion-roi-card">
      <div className="roi-card-header">
        <span className="roi-rank">#{rank}</span>
        <Tag type="purple" size="sm">
          {promotion.promo_code}
        </Tag>
      </div>
      <div className="roi-card-stats">
        <div className="roi-stat">
          <strong>Usage:</strong> {promotion.usage_count}{" "}
          {promotion.usage_count === 1 ? "time" : "times"}
        </div>
        <div className="roi-stat">
          <strong>Revenue:</strong> {formatCurrency(promotion.total_revenue)}
        </div>
        <div className="roi-stat">
          <strong>ROI:</strong> {promotion.roi_percentage.toFixed(1)}%
        </div>
      </div>
    </div>
  );
}

export default PromotionROICard;
