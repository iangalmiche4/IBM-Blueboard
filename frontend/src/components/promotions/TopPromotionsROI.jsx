import { Column, Grid } from "@carbon/react";
import PromotionROICard from "./PromotionROICard";

/**
 * TopPromotionsROI - Display top performing promotions by ROI
 * Shows up to 3 best performing promotions with their metrics
 */
function TopPromotionsROI({ promotions, maxItems = 3 }) {
  if (!promotions || promotions.length === 0) {
    return null;
  }

  const topPromotions = promotions.slice(0, maxItems);

  return (
    <div className="top-promotions-roi">
      <h4 className="roi-section-title">Top Performing Promotions (ROI)</h4>
      <Grid>
        {topPromotions.map((promo, index) => (
          <Column key={promo.id || promo.promo_code} sm={4} md={4} lg={4}>
            <PromotionROICard promotion={promo} rank={index + 1} />
          </Column>
        ))}
      </Grid>
    </div>
  );
}

export default TopPromotionsROI;
