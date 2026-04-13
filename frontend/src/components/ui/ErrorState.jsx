import { InlineNotification } from "@carbon/react";

function ErrorState({ message = "An error occurred", onRetry }) {
  return (
    <div className="page-container">
      <InlineNotification
        kind="error"
        title="Error"
        subtitle={message}
        lowContrast
        actions={
          onRetry
            ? {
                onClick: onRetry,
                label: "Retry",
              }
            : undefined
        }
      />
    </div>
  );
}

export default ErrorState;
