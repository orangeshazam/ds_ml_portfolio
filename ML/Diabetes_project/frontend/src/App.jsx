// Root layout — centered landing page card with title and prediction form.

import PredictionForm from "./components/PredictionForm";

function App() {
  return (
    <main className="page">
      <div className="card">
        <header className="card-header">
          <h1>Diabetes Risk Predictor</h1>
          <p className="subtitle">Enter your health metrics to check your diabetes risk</p>
        </header>
        <PredictionForm />
      </div>
    </main>
  );
}

export default App;
