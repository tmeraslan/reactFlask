
import React, { useState } from "react";
import styles from "./styles";


// אפשר לשנות ב-.env אם תרצה:
// VITE_API_BASE=http://localhost:5000
// const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5000";

// const API_BASE = import.meta.env.VITE_API_BASE || window.location.origin;
const API_BASE = "http://localhost:8080"


const CURRENCIES = ["USD", "EUR", "GBP", "JPY"];

export default function App() {
  const [amount, setAmount] = useState("100");
  const [fromCur, setFromCur] = useState("USD");
  const [toCur, setToCur] = useState("EUR");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    const numericAmount = Number(amount);
    if (isNaN(numericAmount)) {
      setError("Amount must be a number");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/convert`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          amount: numericAmount,
          from: fromCur,
          to: toCur,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || `HTTP ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1>Currency Converter</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.field}>
            <label>Amount:</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              step="0.01"
            />
          </div>

          <div style={styles.fieldRow}>
            <div style={styles.field}>
              <label>From:</label>
              <select value={fromCur} onChange={(e) => setFromCur(e.target.value)}>
                {CURRENCIES.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            <div style={styles.field}>
              <label>To:</label>
              <select value={toCur} onChange={(e) => setToCur(e.target.value)}>
                {CURRENCIES.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? "Converting..." : "Convert"}
          </button>
        </form>

        {error && <p style={{ color: "red", marginTop: "10px" }}>Error: {error}</p>}

        {result && (
          <div style={styles.resultBox}>
            <p>
              {result.amount} {result.from} =&gt;{" "}
              <strong>
                {result.result} {result.to}
              </strong>
            </p>
            {result.rate && (
              <p>
                Rate: 1 {result.from} = {result.rate} {result.to}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
