import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/events")
      .then((response) => response.json())
      .then((data) => setEvents(data))
      .catch((error) => {
        console.error("Failed to load events:", error);
      });
  }, []);

  const loadEventDetails = (eventId) => {
    fetch(`http://127.0.0.1:8000/events/${eventId}`)
      .then((response) => response.json())
      .then((data) => setSelectedEvent(data))
      .catch((error) => {
        console.error("Failed to load event details:", error);
      });
  };

  return (
    <div className="app">
      <header>
        <div>
          <h1>TraceLite</h1>
          <p>Application error monitoring</p>
        </div>
      </header>

      <main>
        <section>
          <h2>Issues</h2>
          <p>Errors captured from your applications appear here.</p>

          {events.length === 0 ? (
            <div className="empty-state">
              <h3>No issues found</h3>
              <p>Send an error through the TraceLite SDK to create one.</p>
            </div>
          ) : (
            <div className="issues-list">
              {events.map((event) => (
                <button
                  className="issue-card"
                  key={event.id}
                  onClick={() => loadEventDetails(event.id)}
                >
                  <div>
                    <h3>{event.type}</h3>
                    <p>{event.message}</p>
                  </div>

                  <div className="issue-meta">
                    <span>{event.app_name}</span>
                    <span>{event.environment}</span>
                    <span>{event.occurrence_count} occurrences</span>
                  </div>
                </button>
              ))}
            </div>
          )}

          {selectedEvent && (
            <div className="issue-details">
              <h2>Issue details</h2>

              <p>
                <strong>Type:</strong> {selectedEvent.type}
              </p>

              <p>
                <strong>Message:</strong> {selectedEvent.message}
              </p>

              <p>
                <strong>Application:</strong> {selectedEvent.app_name}
              </p>

              <p>
                <strong>Environment:</strong> {selectedEvent.environment}
              </p>

              <p>
                <strong>Occurrences:</strong> {selectedEvent.occurrence_count}
              </p>

              <p>
                <strong>Last seen:</strong> {selectedEvent.timestamp}
              </p>

              <h3>Stack trace</h3>

              <pre>{selectedEvent.stack_trace}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;