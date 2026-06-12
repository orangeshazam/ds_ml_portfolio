# Diabetes Risk Predictor

A web application where users enter eight health metrics and receive a diabetes risk prediction powered by a pre-trained **Support Vector Machine (SVM)** model. The backend scales inputs with a saved **StandardScaler** before inference, and the frontend is a single centered landing page with a frosted-glass form card over a nature background.

## Project Structure

```
Diabetes_project/
├── backend/          # Flask API and model artifacts
├── frontend/         # React landing page
├── training/         # Dataset, notebook, and model training script
├── docs/             # Project rules and documentation
└── README.md
```

## Model Files

The app requires two pickle files in `backend/model/`:

| File | Description |
|------|-------------|
| `diabetes_prediction.pickle` | Trained linear-kernel SVM classifier |
| `scaler.pickle` | Fitted `StandardScaler` (required — predictions are wrong without it) |
| `columns.json` | Feature column names in prediction order |

### How to generate the pickle files

From the project root:

```bash
pip install pandas scikit-learn
python training/train_model.py
```

This reads `training/diabetes.csv` and writes all three files to `backend/model/`.

> **Note:** `.pickle` files are listed in `.gitignore` and are not committed to version control.

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Flask runs on **http://localhost:5000**.

## Frontend Setup

```bash
cd frontend
npm install
npm start
```

React runs on **http://localhost:3000** and calls the Flask API at port 5000.

## Input Features

| Field | Description |
|-------|-------------|
| `pregnancies` | Number of pregnancies |
| `glucose` | Plasma glucose concentration (mg/dL) |
| `bloodpressure` | Diastolic blood pressure (mm Hg) |
| `skinthickness` | Triceps skin fold thickness (mm) |
| `insulin` | 2-hour serum insulin (µU/mL) |
| `bmi` | Body mass index |
| `diabetespedigreefunction` | Diabetes pedigree function (family history score) |
| `age` | Age in years |

## Example API Request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"pregnancies":4,"glucose":110,"bloodpressure":92,"skinthickness":0,"insulin":0,"bmi":37.6,"diabetespedigreefunction":0.191,"age":30}'
```

Expected response:

```json
{"label": "Not Diabetic", "prediction": 0}
```
