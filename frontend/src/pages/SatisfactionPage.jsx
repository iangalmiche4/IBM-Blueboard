import { Star, StarFilled } from "@carbon/icons-react";
import { Column, Grid, Tile } from "@carbon/react";
import { DataTableWrapper } from "../components/shared";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { API_CONFIG } from "../config/api";
import { useFetchData } from "../hooks";
import { apiClient } from "../services/api/";
import { formatDate } from "../utils/formatters";

function SatisfactionPage() {
  const {
    data: reviews,
    loading: reviewsLoading,
    error: reviewsError,
    refetch: refetchReviews,
  } = useFetchData(
    () => apiClient.get(`/satisfaction/?limit=${API_CONFIG.DEFAULT_LIMIT}`),
    [],
  );

  const {
    data: stats,
    loading: statsLoading,
    error: statsError,
  } = useFetchData(() => apiClient.get("/analytics/satisfaction-stats"), []);

  const headers = [
    { key: "product_name", header: "Product", isSortable: true },
    { key: "customer_name", header: "Customer", isSortable: true },
    { key: "overall_rating", header: "Rating", isSortable: true },
    { key: "review_date", header: "Date", isSortable: true },
    { key: "comment", header: "Comment", isSortable: false },
  ];

  const loading = reviewsLoading || statsLoading;
  const error = reviewsError || statsError;

  const renderStars = (rating) => {
    return (
      <div className="satisfaction-page__stars">
        {[1, 2, 3, 4, 5].map((star) =>
          star <= rating ? (
            <StarFilled key={star} size={16} className="star-filled" />
          ) : (
            <Star key={star} size={16} className="star-empty" />
          ),
        )}
      </div>
    );
  };

  const rowMapper = (review) => ({
    id: review.id,
    product_name: review.product_id
      ? review.product_id.substring(0, 8) + "..."
      : "N/A",
    customer_name: review.customer_id
      ? review.customer_id.substring(0, 8) + "..."
      : "N/A",
    overall_rating: renderStars(review.overall_rating),
    review_date: formatDate(review.review_date),
    comment: review.comment
      ? review.comment.substring(0, 100) + "..."
      : "No comment",
  });

  if (loading) return <LoadingState message="Loading satisfaction data..." />;
  if (error) return <ErrorState message={error} onRetry={refetchReviews} />;

  const reviewsData = Array.isArray(reviews) ? reviews : [];

  // Rating breakdown data for display
  const ratingBreakdown = stats?.average_ratings || {
    overall: 0,
    quality: 0,
    price: 0,
    packaging: 0,
    delivery: 0,
  };

  const overallScore = ratingBreakdown.overall || 0;
  const scorePercentage = (overallScore / 5) * 100;

  // Determine CSS class for progress bar based on score
  const getScoreClass = (score) => {
    const percentage = (score / 5) * 100;

    if (percentage >= 80) return "satisfaction-page__score-bar-fill--excellent";
    if (percentage >= 60) return "satisfaction-page__score-bar-fill--good";
    if (percentage >= 40) return "satisfaction-page__score-bar-fill--fair";
    return "satisfaction-page__score-bar-fill--poor";
  };

  return (
    <div className="page-container">
      <PageHeader
        title="Customer Satisfaction"
        subtitle="Monitor and analyze customer feedback and ratings"
      />

      {/* Stats */}
      <div className="satisfaction-page__stats">
        <Grid narrow>
          <Column sm={4} md={8} lg={8}>
            <Tile className="satisfaction-page__score-tile">
              <h4>Average Satisfaction Score</h4>
              <div className="satisfaction-page__score-value">
                {overallScore.toFixed(2)}
              </div>
              <div className="satisfaction-page__score-label">out of 5.00</div>
              <div className="satisfaction-page__score-bar">
                <div
                  className={`satisfaction-page__score-bar-fill ${getScoreClass(overallScore)}`}
                  style={{ width: `${scorePercentage}%` }}
                />
              </div>
              <div className="satisfaction-page__score-percentage">
                {scorePercentage.toFixed(0)}% satisfaction rate
              </div>
            </Tile>
          </Column>
          <Column sm={4} md={8} lg={8}>
            <Tile className="satisfaction-page__breakdown-tile">
              <h4>Rating Breakdown</h4>
              <div className="satisfaction-page__breakdown-grid">
                <div className="satisfaction-page__breakdown-item">
                  <span>Quality:</span>
                  <strong>
                    {ratingBreakdown.quality?.toFixed(2) || "0.00"}/5
                  </strong>
                </div>
                <div className="satisfaction-page__breakdown-item">
                  <span>Price:</span>
                  <strong>
                    {ratingBreakdown.price?.toFixed(2) || "0.00"}/5
                  </strong>
                </div>
                <div className="satisfaction-page__breakdown-item">
                  <span>Packaging:</span>
                  <strong>
                    {ratingBreakdown.packaging?.toFixed(2) || "0.00"}/5
                  </strong>
                </div>
                <div className="satisfaction-page__breakdown-item">
                  <span>Delivery:</span>
                  <strong>
                    {ratingBreakdown.delivery?.toFixed(2) || "0.00"}/5
                  </strong>
                </div>
              </div>
            </Tile>
          </Column>
        </Grid>
      </div>

      {/* Reviews Table */}
      <DataTableWrapper
        data={reviewsData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search reviews..."
        initialSort={{ key: "review_date", direction: "DESC" }}
        exportFilename="satisfaction"
        exportTitle="Customer Reviews"
        tableId="satisfaction-table"
        exportMapper={(review) => ({
          product_name: review.product_id
            ? review.product_id.substring(0, 8) + "..."
            : "N/A",
          customer_name: review.customer_id
            ? review.customer_id.substring(0, 8) + "..."
            : "N/A",
          overall_rating: `${review.overall_rating}/5`,
          review_date: formatDate(review.review_date),
          comment: review.comment
            ? review.comment.substring(0, 100) + "..."
            : "No comment",
        })}
      />
    </div>
  );
}

export default SatisfactionPage;
