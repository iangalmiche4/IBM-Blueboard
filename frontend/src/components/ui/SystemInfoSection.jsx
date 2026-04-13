/**
 * SystemInfoSection - Component for displaying a section of system information
 */
import { useEffect, useState } from "react";
import { Checkmark, Close } from "@carbon/icons-react";
import { Column, Grid, SkeletonText, Tile } from "@carbon/react";
import SystemInfoItem from "./SystemInfoItem";
import { systemAPI } from "../../services/api/";

function SystemInfoSection() {
  const [systemInfo, setSystemInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSystemInfo = async () => {
      try {
        setLoading(true);
        const response = await systemAPI.getInfo();
        setSystemInfo(response.data);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch system info:", err);
        setError("Failed to load system information");
      } finally {
        setLoading(false);
      }
    };

    fetchSystemInfo();
  }, []);

  const getStatusIcon = (status) => {
    return status === "connected" ? (
      <Checkmark size={20} />
    ) : (
      <Close size={20} />
    );
  };

  if (loading) {
    return (
      <Tile className="system-info-section">
        <h3 className="system-info-section__title">System Information</h3>
        <Grid narrow>
          <Column sm={4} md={4} lg={8}>
            <SkeletonText
              heading
              className="system-info-section__skeleton-item"
            />
            <SkeletonText />
            <SkeletonText />
          </Column>
          <Column sm={4} md={4} lg={8}>
            <SkeletonText
              heading
              className="system-info-section__skeleton-item"
            />
            <SkeletonText />
            <SkeletonText />
          </Column>
        </Grid>
      </Tile>
    );
  }

  if (error) {
    return (
      <Tile className="system-info-section">
        <h3 className="system-info-section__title">System Information</h3>
        <div className="system-info-section__error">{error}</div>
      </Tile>
    );
  }

  if (!systemInfo) return null;

  return (
    <Tile className="system-info-section">
      <h3 className="system-info-section__title">System Information</h3>
      <Grid narrow>
        {/* Left Column */}
        <Column sm={4} md={4} lg={8}>
          <div className="system-info-section__column">
            <SystemInfoItem label="Version" value={systemInfo.version} />
            <SystemInfoItem label="Build Date" value={systemInfo.build_date} />
            <SystemInfoItem
              label="API Status"
              value={
                systemInfo.api_status === "connected"
                  ? "Connected"
                  : "Disconnected"
              }
              icon={getStatusIcon(systemInfo.api_status)}
            />
            <SystemInfoItem
              label="Database"
              value={`${systemInfo.database.type} ${systemInfo.database.version}`}
              icon={getStatusIcon(systemInfo.database.status)}
            />
          </div>
        </Column>

        {/* Right Column */}
        <Column sm={4} md={4} lg={8}>
          <div className="system-info-section__column">
            <SystemInfoItem
              label="Total Records"
              value={systemInfo.database.total_records.toLocaleString()}
            />
            <SystemInfoItem
              label="Environment"
              value={
                systemInfo.environment.charAt(0).toUpperCase() +
                systemInfo.environment.slice(1)
              }
            />
            <SystemInfoItem
              label="Python Version"
              value={systemInfo.python_version}
            />
            <SystemInfoItem
              label="Last Updated"
              value={new Date(systemInfo.last_updated).toLocaleString()}
            />
          </div>
        </Column>
      </Grid>
    </Tile>
  );
}

export default SystemInfoSection;
