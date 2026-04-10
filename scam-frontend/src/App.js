import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("analyze");
  const [darkMode, setDarkMode] = useState(false);

  // ----- ANALYZE TAB -----
  const [message, setMessage] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // ----- LOOKUP TAB -----
  const [lookupPhone, setLookupPhone] = useState("");
  const [lookupEmail, setLookupEmail] = useState("");
  const [lookupResults, setLookupResults] = useState([]);
  const [lookupLoading, setLookupLoading] = useState(false);

  // ----- DASHBOARD -----
  const [allReports, setAllReports] = useState([]);
  const [dashboardLoading, setDashboardLoading] = useState(false);

  const BACKEND_URL = "http://127.0.0.1:8000";

  // ---------------------------------------------------------------
  //  ANALYZE MESSAGE
  // ---------------------------------------------------------------
  const analyzeMessage = async () => {
    if (!message.trim()) {
      alert("Please enter a message.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${BACKEND_URL}/analyze_message`, {
        message,
        phone: phone || null,
        email: email || null,
        source: "webapp",
      });

      setResult(response.data);
    } catch (error) {
      console.log(error);
      alert("Backend error — is FastAPI running?");
    }

    setLoading(false);
  };

  const reportScam = async () => {
    if (!result) return;

    try {
      await axios.post(`${BACKEND_URL}/report_scam`, {
        message_text: message,
        label: result.label,
        confidence: result.confidence,
        phone: phone || null,
        email: email || null,
        source: "webapp",
      });

      alert("Report saved successfully!");
    } catch (error) {
      alert("Error saving scam report.");
    }
  };

  // ---------------------------------------------------------------
  //  LOOKUP CONTACT HISTORY
  // ---------------------------------------------------------------
  const lookupContactHistory = async () => {
    if (!lookupPhone && !lookupEmail) {
      alert("Enter phone or email.");
      return;
    }

    setLookupLoading(true);

    try {
      const params = new URLSearchParams();
      if (lookupPhone) params.append("phone", lookupPhone);
      if (lookupEmail) params.append("email", lookupEmail);

      const response = await axios.get(
        `${BACKEND_URL}/reports/by_contact?${params.toString()}`
      );

      setLookupResults(response.data);
    } catch (error) {
      alert("Error reading contact history.");
    }

    setLookupLoading(false);
  };

  // ---------------------------------------------------------------
  //  DASHBOARD
  // ---------------------------------------------------------------
  const fetchAllReports = async () => {
    setDashboardLoading(true);
    try {
      const response = await axios.get(`${BACKEND_URL}/reports/all`);
      setAllReports(response.data);
    } catch (err) {
      alert("Error loading dashboard data.");
    }
    setDashboardLoading(false);
  };

  useEffect(() => {
    if (activeTab === "dashboard") {
      fetchAllReports();
    }
  }, [activeTab]);

  const appClass = darkMode ? "app dark" : "app light";

  // ---------------------------------------------------------------
  //  UI STARTS HERE
  // ---------------------------------------------------------------
  return (
    <div className={appClass}>
      {/* NAVBAR */}
      <div className="navBar">
        <span className="logoText">AI Job Scam Detection</span>

        <div className="navCenter">
          <button
            className={activeTab === "analyze" ? "navBtn active" : "navBtn"}
            onClick={() => setActiveTab("analyze")}
          >
            Analyze
          </button>
          <button
            className={activeTab === "lookup" ? "navBtn active" : "navBtn"}
            onClick={() => setActiveTab("lookup")}
          >
            Check History
          </button>
          <button
            className={activeTab === "dashboard" ? "navBtn active" : "navBtn"}
            onClick={() => setActiveTab("dashboard")}
          >
            Dashboard
          </button>
        </div>

        <button className="darkToggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "☀️ Light" : "🌙 Dark"}
        </button>
      </div>

      {/* MAIN CONTAINER */}
      <div className="container">

        {/* ===========================================================
            ANALYZE TAB
        =========================================================== */}
        {activeTab === "analyze" && (
          <>
            <h1 className="title">Analyze Job Message</h1>

            <textarea
              className="inputBox"
              placeholder="Paste any job or course message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <div className="row">
              <input
                className="smallInput"
                placeholder="Phone (optional)"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
              <input
                className="smallInput"
                placeholder="Email (optional)"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <button className="analyzeBtn" onClick={analyzeMessage}>
              {loading ? "Analyzing..." : "Analyze Message"}
            </button>

            {/* SHOW RESULT */}
            {result && (
              <div className="resultBox">
                {/* COLOR BASED ON LABEL */}
                {(() => {
                  let color = "white";
                  if (result.label === "scam") color = "red";
                  else if (result.label === "course") color = "orange";
                  else color = "green";

                  return (
                    <h2 style={{ color }}>
                      {result.label.toUpperCase()}
                    </h2>
                  );
                })()}

                <p>
                  <b>Confidence:</b> {(result.confidence * 100).toFixed(2)}%
                </p>

                <h3>Risk Reasons:</h3>
                <ul>
                  {result.risk_reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>

                <h3>Advice:</h3>
                <p className="advice">{result.advice}</p>

                <h3>Complaint Template:</h3>
                <pre className="complaint">{result.complaint_template}</pre>

                <p><b>Reports for phone:</b> {result.known_reports_count_for_phone}</p>
                <p><b>Reports for email:</b> {result.known_reports_count_for_email}</p>

                <button className="reportBtn" onClick={reportScam}>
                  Report Scam
                </button>
              </div>
            )}
          </>
        )}

        {/* ===========================================================
            LOOKUP TAB (REPUTATION SYSTEM)
        =========================================================== */}
        {activeTab === "lookup" && (
          <>
            <h1 className="title">Check Contact History</h1>

            <div className="row">
              <input
                className="smallInput"
                placeholder="Phone"
                value={lookupPhone}
                onChange={(e) => setLookupPhone(e.target.value)}
              />
              <input
                className="smallInput"
                placeholder="Email"
                value={lookupEmail}
                onChange={(e) => setLookupEmail(e.target.value)}
              />
            </div>

            <button className="analyzeBtn" onClick={lookupContactHistory}>
              {lookupLoading ? "Searching..." : "Search"}
            </button>

            {/* RESULT BOX */}
            <div className="resultBox">
              {(() => {
                const scamCount = lookupResults.filter(r => r.label === "scam").length;
                const legitCount = lookupResults.filter(r => r.label === "legit").length;
                const courseCount = lookupResults.filter(r => r.label === "course").length;

                let reputation = "No History Found";
                let color = "gray";

                if (scamCount >= 3) {
                  reputation = "HIGH RISK (Scam)";
                  color = "red";
                } else if (scamCount >= 1) {
                  reputation = "Suspicious";
                  color = "orange";
                } else if (courseCount >= 2) {
                  reputation = "Course Provider / Paid Training";
                  color = "orange";
                } else if (legitCount >= 2) {
                  reputation = "Likely Legitimate";
                  color = "green";
                }

                return (
                  <>
                    <h2 style={{ color }}>{reputation}</h2>
                    <p><b>Scam Reports:</b> {scamCount}</p>
                    <p><b>Course Reports:</b> {courseCount}</p>
                    <p><b>Legit Reports:</b> {legitCount}</p>

                    {lookupResults.length > 0 ? (
                      <table className="table">
                        <thead>
                          <tr>
                            <th>ID</th>
                            <th>Label</th>
                            <th>Confidence</th>
                            <th>Phone</th>
                            <th>Email</th>
                          </tr>
                        </thead>
                        <tbody>
                          {lookupResults.map((r) => (
                            <tr key={r.id}>
                              <td>{r.id}</td>
                              <td>{r.label}</td>
                              <td>{(r.confidence * 100).toFixed(1)}%</td>
                              <td>{r.phone || "-"}</td>
                              <td>{r.email || "-"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    ) : (
                      <p>No reports found.</p>
                    )}
                  </>
                );
              })()}
            </div>
          </>
        )}

        {/* ===========================================================
            DASHBOARD TAB
        =========================================================== */}
        {activeTab === "dashboard" && (
          <>
            <h1 className="title">Dashboard</h1>

            {dashboardLoading ? (
              <p>Loading...</p>
            ) : (
              <>
                <div className="statsRow">
                  <div className="statCard">
                    <h2>{allReports.length}</h2>
                    <p>Total Reports</p>
                  </div>
                  <div className="statCard">
                    <h2>{allReports.filter(r => r.label === "scam").length}</h2>
                    <p>Scam Reports</p>
                  </div>
                  <div className="statCard">
                    <h2>{allReports.filter(r => r.label === "course").length}</h2>
                    <p>Course Reports</p>
                  </div>
                  <div className="statCard">
                    <h2>{allReports.filter(r => r.label === "legit").length}</h2>
                    <p>Legit Reports</p>
                  </div>
                </div>

                <div className="resultBox">
                  <h3>Recent Reports</h3>

                  <table className="table">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Label</th>
                        <th>Confidence</th>
                        <th>Phone</th>
                        <th>Email</th>
                      </tr>
                    </thead>
                    <tbody>
                      {allReports.slice(0, 10).map((r) => (
                        <tr key={r.id}>
                          <td>{r.id}</td>
                          <td>{r.label}</td>
                          <td>{(r.confidence * 100).toFixed(1)}%</td>
                          <td>{r.phone || "-"}</td>
                          <td>{r.email || "-"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
