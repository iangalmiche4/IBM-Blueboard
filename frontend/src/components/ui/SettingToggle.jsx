import { Column, Toggle } from "@carbon/react";

/**
 * Reusable Toggle component for settings
 * @param {string} id - Unique identifier
 * @param {string} label - Label text
 * @param {boolean} toggled - Current toggle state
 * @param {Function} onToggle - Toggle handler
 * @param {Object} columnProps - Props for the Column wrapper (sm, md, lg)
 */
function SettingToggle({
  id,
  label,
  toggled,
  onToggle,
  columnProps = { sm: 4, md: 8, lg: 16 },
}) {
  return (
    <Column {...columnProps}>
      <Toggle
        id={id}
        labelText={label}
        labelA="Off"
        labelB="On"
        toggled={toggled}
        onToggle={onToggle}
      />
    </Column>
  );
}

export default SettingToggle;
