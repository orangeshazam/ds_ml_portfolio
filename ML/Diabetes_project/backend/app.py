# Flask API server for diabetes risk predictions using the trained SVM model.

from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.predictor import predict

app = Flask(__name__)
CORS(app)


@app.route("/api/predict", methods=["POST"])
def predict_route():
    try:
        data = request.get_json()
        result, error = predict(data)

        if error:
            return jsonify({"error": error}), 400

        return jsonify(result), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
