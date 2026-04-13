import { DraggableWidget } from "./";

/**
 * WidgetContainer - Interface component to simplify widget addition
 * Wraps content in a draggable widget with proper structure for react-grid-layout
 *
 * @param {string} id - Unique identifier for the widget (must match layout config)
 * @param {React.ReactNode} children - Widget content to render
 */
function WidgetContainer({ id, children }) {
  return <DraggableWidget id={id}>{children}</DraggableWidget>;
}

export default WidgetContainer;
