import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Clean Markdown returned by the AI
  const cleanMarkdown = (text) => {
    if (!text) return "";

    const lines = text.split("\n");
    const sectionNames = [
      "Trip Summary",
      "Day-by-Day Itinerary",
      "Flight Information",
      "Accommodation",
      "Activities",
      "Safety Tips",
      "Budget Summary",
      "Money-Saving Suggestions",
    ];
    const sectionRegex = new RegExp(
      `^(?:###?\\s*)?\\*\\*(${sectionNames.join("|")})\\*\\*:?\\s*$`,
      "i"
    );

    const processedLines = lines.map((line) => {
      // Never alter table rows or content inside tables
      if (line.trim().startsWith("|")) {
        return line;
      }
      // Convert standalone bold section headers into markdown ## headings
      const match = line.trim().match(sectionRegex);
      if (match) {
        return `\n## ${match[1]}\n`;
      }
      return line;
    });

    let cleaned = processedLines
      .join("\n")
      // Remove escaped backslashes
      .replace(/\\\\/g, "")
      // Remove unnecessary TravelMind heading
      .replace(/^###\s*\*TravelMind AI\*$/gim, "")
      // Remove excessive blank lines
      .replace(/\n{3,}/g, "\n\n")
      .trim();

    return cleaned;
  };

  // Send request to FastAPI backend
  const sendMessage = async () => {
    if (loading || !message.trim()) return;

    setLoading(true);
    setResponse("");
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request: message,
        }),
      });

      let data = null;
      try {
        data = await res.json();
      } catch {
        data = null;
      }

      if (!res.ok) {
        let errorMsg = "";

        if (data) {
          if (typeof data.detail === "string") {
            errorMsg = data.detail;
          } else if (typeof data.message === "string") {
            errorMsg = data.message;
          } else if (typeof data.error === "string") {
            errorMsg = data.error;
          } else if (Array.isArray(data.detail)) {
            errorMsg = data.detail.map((d) => d.msg || JSON.stringify(d)).join(", ");
          } else if (typeof data.detail === "object" && data.detail !== null) {
            errorMsg = data.detail.message || JSON.stringify(data.detail);
          }
        }

        if (!errorMsg) {
          if (res.status === 429) {
            errorMsg =
              "The Gemini API request quota has been exhausted (HTTP 429: RESOURCE_EXHAUSTED). Please wait a few moments before trying again.";
          } else {
            errorMsg = `Server error (${res.status}): ${res.statusText || "Unable to complete request"}`;
          }
        }

        throw new Error(errorMsg);
      }

      const result =
        data.plan ||
        data.response ||
        data.final_plan ||
        data.message ||
        JSON.stringify(data, null, 2);

      setResponse(cleanMarkdown(result));
    } catch (err) {
      let displayMessage = err.message;
      if (err.message === "Failed to fetch") {
        displayMessage =
          "Unable to connect to the backend server. Please verify that the FastAPI backend is running on http://127.0.0.1:8000.";
      }
      setError(displayMessage);
    } finally {
      setLoading(false);
    }
  };

  // Quick trip buttons
  const selectTrip = (trip) => {
    if (loading) return;
    setMessage(trip);
    setError("");
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div className="logo">
          ✈️ <span>TravelMind AI</span>
        </div>

        <p>Your AI-powered travel planner</p>
      </header>


      <main className="chat-container">

        {/* WELCOME SCREEN */}
        {!response && !error && !loading && (
          <div className="welcome">

            <div className="welcome-icon">
              🌍
            </div>

            <h2>
              Plan your perfect trip
            </h2>

            <p>
              Tell me where you want to go,
              your budget, dates, and preferences.
            </p>


            {/* QUICK TRIP OPTIONS */}
            <div className="examples">

              <button
                onClick={() =>
                  selectTrip(
                    "Plan a 5 day trip from Hyderabad to Goa for 2 travelers under ₹30,000. My interests are beaches, adventure, nature, and nightlife."
                  )
                }
              >
                🏖️ Goa trip
              </button>


              <button
                onClick={() =>
                  selectTrip(
                    "Plan a 4 day trip from Hyderabad to Kerala for 2 travelers under ₹25,000. My interests are nature, beaches, food, and culture."
                  )
                }
              >
                🌴 Kerala trip
              </button>


              <button
                onClick={() =>
                  selectTrip(
                    "Plan a 5 day trip from Hyderabad to Manali for 2 travelers under ₹30,000. My interests are mountains, adventure, nature, and sightseeing."
                  )
                }
              >
                🏔️ Manali trip
              </button>

            </div>

          </div>
        )}


        {/* LOADING SCREEN */}
        {loading && (
          <div className="loading-card">

            <div className="loader">
              ✈️
            </div>

            <h2>
              Planning your trip...
            </h2>

            <p>
              TravelMind AI is consulting its travel agents.
            </p>


            <div className="agent-status">

              <div>
                📍 Destination Agent
              </div>

              <div>
                ✈️ Flight Agent
              </div>

              <div>
                🏨 Hotel Agent
              </div>

              <div>
                🎯 Activity Agent
              </div>

              <div>
                🛡️ Safety Agent
              </div>

              <div>
                💰 Budget Agent
              </div>

              <div>
                🧠 Final Planner
              </div>

            </div>

          </div>
        )}


        {/* ERROR DISPLAY */}
        {error && !loading && (
          <div className="error-card">
            <div className="error-header">
              <span className="error-icon">⚠️</span>
              <div>
                <h2>Notice: Request Could Not Be Completed</h2>
                <p>Gemini API Quota / Service Message</p>
              </div>
            </div>

            <div className="error-body">
              <p>{error}</p>
            </div>

            <div className="error-footer">
              <button
                className="error-dismiss-btn"
                onClick={() => setError("")}
              >
                Dismiss
              </button>
            </div>
          </div>
        )}


        {/* TRAVEL PLAN RESULT */}
        {response && !loading && (
          <div className="result-card">

            {/* RESULT HEADER */}
            <div className="result-header">

              <div className="result-title">

                <span className="result-icon">
                  ✈️
                </span>

                <div>

                  <h2>
                    Your Travel Plan
                  </h2>

                  <p>
                    Generated by TravelMind AI
                  </p>

                </div>

              </div>

            </div>


            {/* AI RESPONSE */}
            <div className="result-content">

              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {response}
              </ReactMarkdown>

            </div>


            {/* NEW TRIP BUTTON */}
            <button
              className="new-trip-button"
              onClick={() => {
                setResponse("");
                setMessage("");
                setError("");
              }}
            >
              ✨ Plan Another Trip
            </button>

          </div>
        )}


        {/* INPUT BOX */}
        {!loading && (
          <div className="input-area">

            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Example: Plan a 5-day trip to Goa under ₹30,000..."
              rows={4}
            />


            <button
              className="plan-button"
              onClick={sendMessage}
              disabled={loading || !message.trim()}
            >
              {loading ? "Planning..." : "Plan My Trip ✈️"}
            </button>

          </div>
        )}

      </main>


      {/* FOOTER */}
      <footer>

        <p>
          Powered by{" "}
          <strong>TravelMind AI</strong>
          {" "}• Multi-Agent Travel Planning
        </p>

      </footer>

    </div>
  );
}

export default App;