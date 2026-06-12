// Health metrics form — collects 8 features and calls the Flask prediction API.

import { useState } from "react";
import ResultDisplay from "./ResultDisplay";

const API_URL = "http://localhost:5000/api/predict";

const FORM_FIELDS = [
  { key: "pregnancies", label: "Number of Pregnancies", step: 1, min: 0, max: 20, placeholder: "e.g. 2" },
  { key: "glucose", label: "Glucose Level (mg/dL)", step: 1, min: 0, max: 300, placeholder: "e.g. 110" },
  { key: "bloodpressure", label: "Blood Pressure (mm Hg)", step: 1, min: 0, max: 150, placeholder: "e.g. 72" },
  { key: "skinthickness", label: "Skin Thickness (mm)", step: 1, min: 0, max: 100, placeholder: "e.g. 20" },
  { key: "insulin", label: "Insulin Level (µU/mL)", step: 1, min: 0, max: 900, placeholder: "e.g. 80" },
  { key: "bmi", label: "BMI", step: 0.1, min: 0, max: 70, placeholder: "e.g. 28.5" },
  { key: "diabetespedigreefunction", label: "Diabetes Family History Score", step: 0.001, min: 0, max: 3, placeholder: "e.g. 0.351" },
  { key: "age", label: "Age (years)", step: 1, min: 1, max: 120, placeholder: "e.g. 30" },
];

function PredictionForm() {
  const [formData, setFormData] = useState({
    pregnancies: "",
    glucose: "",
    bloodpressure: "",
    skinthickness: "",
    insulin: "",
    bmi: "",
    diabetespedigreefunction: "",
    age: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || "Prediction failed");
      }
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        {FORM_FIELDS.map((field) => (
          <label key={field.key} className="field">
            <span className="field-label">{field.label}</span>
            <input
              type="number"
              name={field.key}
              value={formData[field.key]}
              onChange={handleChange}
              min={field.min}
              max={field.max}
              step={field.step}
              placeholder={field.placeholder}
              required
            />
          </label>
        ))}
      </div>

      <button type="submit" className="submit-btn" disabled={loading}>
        {loading ? "Predicting..." : "Check Diabetes Risk"}
      </button>

      <ResultDisplay prediction={prediction} loading={loading} error={error} />
    </form>
  );
}

export default PredictionForm;
