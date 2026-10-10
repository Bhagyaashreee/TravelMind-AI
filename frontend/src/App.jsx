import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // Clean Markdown returned by the AI
  const cleanMarkdown = (text) => {
    if (!text) return "";

    let cleaned = text
      // Remove escaped backslashes
      .replace(/\\\\/g, "")

      // Remove unnecessary TravelMind heading
      .replace(/^###\s*\*TravelMind AI\*$/gim, "")

      // Convert important sections into headings
      .replace(
        /\*\*(Trip Summary|Day-by-Day Itinerary|Flight Information|Accommodation|Activities|Safety Tips|Budget Summary|Money-Saving Suggestions)\*\*/gi,
        "\n\n## $1\n\n"
      )

      // Remove excessive blank lines
      .replace(/\n{3,}/g, "\n\n")

      .trim();

    return cleaned;
  };

  // Send request to FastAPI backend
  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResponse("");

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

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.detail || "Something went wrong while generating the plan."
        );
      }

      const result =
        data.plan ||
        data.response ||
        data.final_plan ||
        data.message ||
        JSON.stringify(data, null, 2);

      setResponse(cleanMarkdown(result));
    } catch (error) {
      setResponse(
        `❌ Unable to generate the travel plan.\n\n**Error:** ${error.message}`
      );
    } finally {
      setLoading(false);
    }
  };

  // Quick trip buttons
  const selectTrip = (trip) => {
    setMessage(trip);
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
        {!response && !loading && (
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

              <ReactMarkdown>
                {response}
              </ReactMarkdown>

            </div>


            {/* NEW TRIP BUTTON */}
            <button
              className="new-trip-button"
              onClick={() => {
                setResponse("");
                setMessage("");
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
              disabled={!message.trim()}
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