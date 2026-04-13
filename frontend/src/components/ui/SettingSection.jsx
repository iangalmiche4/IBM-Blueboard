import { AccordionItem, Grid } from "@carbon/react";

/**
 * Reusable section wrapper for settings with AccordionItem and Grid
 * @param {string} title - Section title
 * @param {ReactNode} children - Section content
 */
function SettingSection({ title, children }) {
  return (
    <AccordionItem title={title}>
      <Grid narrow>{children}</Grid>
    </AccordionItem>
  );
}

export default SettingSection;
