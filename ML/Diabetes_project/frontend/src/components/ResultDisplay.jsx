// Displays prediction result, loading state, or API error below the submit button.

function ResultDisplay({ prediction, loading, error }) {
  if (loading) {
    return (
      <div className="result result-loading" aria-live="polite">
        <span className="spinner" aria-hidden="true" />
        Predicting...
      </div>
    );
  }

  if (error) {
    return (
      <div className="result result-error" role="alert">
        {error}
      </div>
    );
  }

  if (!prediction) {
    return null;
  }

  const isDiabetic = prediction.prediction === 1;

  return (
    <div
      className={`result ${isDiabetic ? "result-diabetic" : "result-not-diabetic"}`}
      aria-live="polite"
    >
      {isDiabetic ? "⚠️ Diabetic" : "✅ Not Diabetic"}
    </div>
  );
}

export default ResultDisplay;
