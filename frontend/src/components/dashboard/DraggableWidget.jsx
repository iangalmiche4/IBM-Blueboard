import { Draggable } from "@carbon/icons-react";

/**
 * DraggableWidget - Wrapper for dashboard widgets with drag handle
 */
function DraggableWidget({ children, id }) {
  return (
    <div className="draggable-widget-wrapper" data-widget-id={id}>
      <div className="drag-handle" title="Drag to reposition">
        <Draggable />
      </div>
      <div className="widget-content">{children}</div>
    </div>
  );
}

export default DraggableWidget;
