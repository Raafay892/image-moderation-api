import React, { useState } from "react";

function App() {
  const [token, setToken] = useState("");
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!token) {
      setError("Please enter a token");
      return;
    }
    if (!file) {
      setError("Please select an image file");
      return;
    }
    setError("");
    setLoading(true);
    setReport(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:7000/moderate", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || "Failed to moderate image");
        setLoading(false);
        return;
      }
      const data = await res.json();
      setReport(data);
    } catch (err) {
      setError("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "Arial" }}>
      <h2>Image Moderation UI</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Bearer Token:
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            style={{ width: "100%", marginBottom: "1rem" }}
            placeholder="Enter your API token"
          />
        </label>
        <label>
          Select Image:
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ display: "block", margin: "1rem 0" }}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Moderating..." : "Moderate Image"}
        </button>
      </form>

      {error && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          <strong>{error}</strong>
        </div>
      )}

      {report && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Moderation Report</h3>
          <ul>
            {report.categories.map((cat, i) => (
              <li key={i}>
                <strong>{cat.category}:</strong> {(cat.confidence * 100).toFixed(1)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
