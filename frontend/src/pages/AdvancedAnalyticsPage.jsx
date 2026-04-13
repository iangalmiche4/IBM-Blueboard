import { Money, Purchase, Star, UserMultiple } from "@carbon/icons-react";
import { Column, Grid, Tile } from "@carbon/react";
import { InsightCard, ProgressSection, StatCard } from "../components/shared";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { useAdvancedAnalyticsData } from "../hooks";
import { formatCurrency, formatNumber } from "../utils/formatters";

function AdvancedAnalyticsPage() {
  const {
    loading,
    error,
    stats,
    topProducts,
    segmentData,
    channelData,
    refetch,
  } = useAdvancedAnalyticsData();

  if (loading) return <LoadingState message="Loading advanced analytics..." />;
  if (error) return <ErrorState message={error} onRetry={refetch} />;

  const maxChannelRevenue = Math.max(...channelData.map((c) => c.revenue));
  const maxSegmentCount = Math.max(...segmentData.map((s) => s.count));

  return (
    <div className="page-container">
      <PageHeader
        title="Advanced Analytics"
        subtitle="Deep insights into product performance, customer behavior, and revenue patterns"
      />

      {/* KPI Tiles */}
      <Grid narrow className="mb-2">
        <Column sm={4} md={2} lg={4}>
          <StatCard
            icon={Purchase}
            title="Avg Price"
            value={formatCurrency(stats.avgPrice)}
            subtitle="All products"
            iconColor="#0f62fe"
          />
        </Column>
        <Column sm={4} md={2} lg={4}>
          <StatCard
            icon={Star}
            title="Avg Rating"
            value={`${stats.avgRating}/5`}
            subtitle="Customer satisfaction"
            iconColor="#0f62fe"
          />
        </Column>
        <Column sm={4} md={2} lg={4}>
          <StatCard
            icon={Money}
            title="Total Revenue"
            value={formatCurrency(Math.round(stats.totalRevenue))}
            subtitle="From all sales"
            iconColor="#0f62fe"
          />
        </Column>
        <Column sm={4} md={2} lg={4}>
          <StatCard
            icon={UserMultiple}
            title="Active Customers"
            value={formatNumber(stats.activeCustomers)}
            subtitle="Currently active"
            iconColor="#0f62fe"
          />
        </Column>
      </Grid>

      {/* Top Products */}
      <Grid narrow className="mb-2">
        <Column sm={4} md={8} lg={8}>
          <ProgressSection
            title="Top 5 Products by Revenue"
            items={topProducts}
            getLabel={(product, index) => `${index + 1}. ${product.name}`}
            getValue={(product) => formatCurrency(Math.round(product.revenue))}
            getPercentage={(product) =>
              (product.revenue / topProducts[0].revenue) * 100
            }
          />
        </Column>

        {/* Customer Segments */}
        <Column sm={4} md={8} lg={8}>
          <ProgressSection
            title="Customer Segment Distribution"
            items={segmentData}
            getLabel={(segment) => segment.segment}
            getValue={(segment) => `${segment.count} customers`}
            getPercentage={(segment) => (segment.count / maxSegmentCount) * 100}
          />
        </Column>
      </Grid>

      {/* Channel Performance */}
      <Grid narrow className="mb-2">
        <Column sm={4} md={8} lg={16}>
          <ProgressSection
            title="Revenue by Sales Channel"
            items={channelData}
            getLabel={(channel) => channel.channel}
            getValue={(channel) => formatCurrency(Math.round(channel.revenue))}
            getPercentage={(channel) =>
              (channel.revenue / maxChannelRevenue) * 100
            }
            colors={["#0f62fe", "#4589ff", "#78a9ff", "#a6c8ff"]}
            height={12}
            labelSize="1rem"
            gap="1.5rem"
          />
        </Column>
      </Grid>

      {/* Insights Section */}
      <Grid narrow>
        <Column sm={4} md={8} lg={16}>
          <Tile className="advanced-analytics__insights-tile">
            <h4>Key Insights</h4>
            <div className="advanced-analytics__insights-grid">
              <InsightCard
                title="Product Performance"
                description={`Top 5 products generate ${stats.totalRevenue > 0 ? ((topProducts.reduce((sum, p) => sum + p.revenue, 0) / stats.totalRevenue) * 100).toFixed(1) : "0"}% of total revenue, indicating strong product concentration.`}
                borderColor="#0f62fe"
              />
              <InsightCard
                title="Customer Segmentation"
                description={`${segmentData[0]?.segment} customers form the largest segment with ${segmentData[0]?.count} members, indicating strong customer retention.`}
                borderColor="#0f62fe"
              />
              <InsightCard
                title="Channel Performance"
                description={`${channelData[0]?.channel} channel drives the majority of revenue with ${formatCurrency(Math.round(channelData[0]?.revenue || 0))}.`}
                borderColor="#0f62fe"
              />
            </div>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
}

export default AdvancedAnalyticsPage;
