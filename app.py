from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            N = float(request.form["N"])
            P = float(request.form["P"])
            K = float(request.form["K"])
            temperature = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
            ph = float(request.form["ph"])
            rainfall = float(request.form["rainfall"])

            features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            scaled_features = scaler.transform(features)
            prediction = model.predict(scaled_features)[0]

        except ValueError:
            error = "Please enter valid numeric values."
        except Exception as e:
            error = f"Something went wrong: {str(e)}"

    return render_template("templates/index.html", prediction=prediction, error=error)


if __name__ == "__main__":
    app.run(debug=True)
