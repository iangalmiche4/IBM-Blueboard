import { Tile } from "@carbon/react";
import ProgressBar from "./ProgressBar";

/**
 * ProgressSection - Reusable section with title and progress bars
 * @param {string} title - Section title
 * @param {Array} items - Array of items to display as progress bars
 * @param {Function} getLabel - Function to get label from item
 * @param {Function} getValue - Function to get value from item
 * @param {Function} getPercentage - Function to calculate percentage from item
 * @param {Array} colors - Array of colors to cycle through (default: blue palette)
 * @param {number} height - Height of progress bars (optional)
 * @param {string} labelSize - Font size for labels (optional)
 * @param {string} gap - Gap between progress bars (default: '1rem')
 */
function ProgressSection({
  title,
  items,
  getLabel,
  getValue,
  getPercentage,
  colors = ["#0f62fe", "#4589ff", "#78a9ff", "#a6c8ff", "#d0e2ff"],
  height,
  labelSize,
  gap = "1rem",
}) {
  return (
    <Tile className="analytics-tile">
      <h4 className="progress-section__title">{title}</h4>
      <div
        className="progress-section__list"
        style={gap !== "1rem" ? { gap } : undefined}
      >
        {items.map((item, index) => (
          <ProgressBar
            key={index}
            label={getLabel(item, index)}
            value={getValue(item)}
            percentage={getPercentage(item)}
            color={colors[index % colors.length]}
            height={height}
            labelSize={labelSize}
          />
        ))}
      </div>
    </Tile>
  );
}

export default ProgressSection;
