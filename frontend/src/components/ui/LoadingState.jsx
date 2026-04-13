import { Loading } from "@carbon/react";

function LoadingState({ message = "Loading data..." }) {
  return (
    <div className="loading-container">
      <Loading description={message} withOverlay={false} />
    </div>
  );
}

export default LoadingState;
