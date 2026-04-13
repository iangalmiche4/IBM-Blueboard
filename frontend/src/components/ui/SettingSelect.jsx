import { Column, Select, SelectItem } from "@carbon/react";

/**
 * Reusable Select component for settings
 * @param {string} id - Unique identifier
 * @param {string} label - Label text
 * @param {string} value - Current value
 * @param {Function} onChange - Change handler
 * @param {Array} options - Array of {value, text} objects
 * @param {boolean} disabled - Whether the select is disabled
 * @param {Object} columnProps - Props for the Column wrapper (sm, md, lg)
 */
function SettingSelect({
  id,
  label,
  value,
  onChange,
  options,
  disabled = false,
  columnProps = { sm: 4, md: 4, lg: 8 },
}) {
  return (
    <Column {...columnProps}>
      <Select
        id={id}
        labelText={label}
        value={value}
        onChange={onChange}
        disabled={disabled}
      >
        {options.map((option) => (
          <SelectItem
            key={option.value}
            value={option.value}
            text={option.text}
          />
        ))}
      </Select>
    </Column>
  );
}

export default SettingSelect;
