// frontend/src/App.jsx
import { useState } from "react";
import "./App.css";

function App() {
  const [age, setAge] = useState("");
  const [sex, setSex] = useState("male");
  const [bmi, setBmi] = useState("");
  const [children, setChildren] = useState("");
  const [smoker, setSmoker] = useState("no");
  const [region, setRegion] = useState("southwest");
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      age: Number(age),
      sex,
      bmi: Number(bmi),
      children: Number(children),
      smoker,
      region,
    };

    try {
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (data.error) {
        alert(`Backend Error: ${data.error}`);
        return;
      }

      if (typeof data.prediction === 'number') {
        setPrediction(data.prediction);
      } else {
        console.error("Unexpected response:", data);
        alert("Received invalid data from backend");
      }
    } catch (err) {
      console.error(err);
      alert("Error calling backend");
    }
  };

  return (
    <div className="app">
      <h1>Insurance Prediction (Linear)</h1>

      <form onSubmit={handleSubmit} className="form">
        <label>
          Age:
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
          />
        </label>

        <label>
          Sex:
          <select value={sex} onChange={(e) => setSex(e.target.value)}>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </label>

        <label>
          BMI:
          <input
            type="number"
            step="0.1"
            value={bmi}
            onChange={(e) => setBmi(e.target.value)}
            required
          />
        </label>

        <label>
          Children:
          <input
            type="number"
            value={children}
            onChange={(e) => setChildren(e.target.value)}
            required
          />
        </label>

        <label>
          Smoker:
          <select
            value={smoker}
            onChange={(e) => setSmoker(e.target.value)}
          >
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>

        <label>
          Region:
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
          >
            <option value="southwest">Southwest</option>
            <option value="southeast">Southeast</option>
            <option value="northwest">Northwest</option>
            <option value="northeast">Northeast</option>
          </select>
        </label>

        <button type="submit">Predict</button>
      </form>

      {prediction !== null && typeof prediction === 'number' && (
        <div className="result">
          <h2>Predicted Charges:</h2>
          <p>₹ {prediction.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}

export default App;
