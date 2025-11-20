

// src/styles.js

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "system-ui, sans-serif",
    background: "#f5f5f5",
  },
  card: {
    background: "white",
    padding: "24px 32px",
    borderRadius: "12px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
    width: "320px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  field: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },
  fieldRow: {
    display: "flex",
    gap: "12px",
  },
  button: {
    marginTop: "8px",
    padding: "8px 12px",
    borderRadius: "6px",
    border: "none",
    cursor: "pointer",
  },
  resultBox: {
    marginTop: "16px",
    padding: "10px",
    borderRadius: "8px",
    background: "#f0f0ff",
  },
};

export default styles;
