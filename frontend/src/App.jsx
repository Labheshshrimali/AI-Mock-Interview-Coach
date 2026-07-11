import { useState, useRef } from "react";
import Dashboard from "./Dashboard";

const API_BASE = "http://localhost:8080";

export default function App() {
  const [activeTab, setActiveTab] = useState("interview"); // 'interview' or 'dashboard'
  const [question, setQuestion] = useState(
    "Tell me about a time you disagreed with a teammate."
  );
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];

      recorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      recorder.onstop = handleStop;

      recorder.start();
      mediaRecorderRef.current = recorder;
      setRecording(true);
      setResult(null);
    } catch (err) {
      alert("Microphone access denied or not available.");
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }

  async function handleStop() {
    setLoading(true);
    const blob = new Blob(chunksRef.current, { type: "audio/webm" });

    const formData = new FormData();
    formData.append("question", question);
    formData.append("audio", blob, "answer.wav");

    try {
      const res = await fetch(`${API_BASE}/session/demo/answer?t=${Date.now()}`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Network response was not ok");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Failed to connect to the backend. Is FastAPI running on port 8080?" });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#f4f7f6",
      padding: "40px 20px",
      fontFamily: "'Inter', sans-serif"
    }}>
      <div style={{ maxWidth: 700, margin: "0 auto" }}>
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          <button onClick={() => setActiveTab("interview")} style={{ background: activeTab === "interview" ? "white" : "transparent", border: "none", padding: "10px 20px", borderRadius: 8, cursor: "pointer", fontWeight: 600 }}>Interview</button>
          <button onClick={() => setActiveTab("dashboard")} style={{ background: activeTab === "dashboard" ? "white" : "transparent", border: "none", padding: "10px 20px", borderRadius: 8, cursor: "pointer", fontWeight: 600 }}>History</button>
        </div>

        {activeTab === "interview" ? (
          <div style={{
            backgroundColor: "white",
            borderRadius: 16,
            boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
            padding: "40px",
            border: "1px solid #eaeaea"
          }}>
            <h1 style={{ fontSize: 28, marginBottom: 8, color: "#1a1a1a", fontWeight: 700 }}>AI Mock Interview Coach</h1>
            <p style={{ color: "#666", marginBottom: 32, fontSize: 15 }}>
              Answer the question out loud to receive AI-powered delivery and content feedback.
            </p>

            <div style={{ marginBottom: 24 }}>
              <label style={{ display: "block", marginBottom: 8, fontWeight: 600, color: "#333", fontSize: 14 }}>
                Interview Question
              </label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={3}
                style={{
                  width: "100%",
                  padding: "12px 16px",
                  borderRadius: 8,
                  border: "1px solid #ccc",
                  fontSize: 15,
                  outline: "none",
                  resize: "vertical",
                  boxSizing: "border-box"
                }}
              />
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 32 }}>
              <button
                onClick={recording ? stopRecording : startRecording}
                style={{
                  padding: "12px 24px",
                  background: recording ? "#ef4444" : "#3b82f6",
                  color: "white",
                  border: "none",
                  borderRadius: 8,
                  cursor: "pointer",
                  fontWeight: 600,
                  fontSize: 15,
                  transition: "background 0.2s",
                  boxShadow: recording ? "0 4px 12px rgba(239, 68, 68, 0.3)" : "0 4px 12px rgba(59, 130, 246, 0.3)"
                }}
              >
                {recording ? "⏹ Stop Recording" : "⏺ Start Recording"}
              </button>
              {recording && (
                <span style={{ color: "#ef4444", fontWeight: 500, display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{
                    width: 10, height: 10, borderRadius: "50%", background: "#ef4444",
                    animation: "pulse 1.5s infinite"
                  }} />
                  Recording...
                </span>
              )}
            </div>

            {loading && (
              <div style={{ padding: 24, textAlign: "center", color: "#666", background: "#f8fafc", borderRadius: 8 }}>
                Processing audio, transcribing, and generating feedback...
              </div>
            )}

            {result && !result.error && (
              <div style={{
                marginTop: 24,
                padding: 24,
                background: "#f8fafc",
                borderRadius: 12,
                border: "1px solid #e2e8f0"
              }}>
                <h3 style={{ marginTop: 0, color: "#1e293b", fontSize: 18 }}>📝 Transcript</h3>
                <p style={{ color: "#475569", lineHeight: 1.6, background: "white", padding: 12, borderRadius: 6, border: "1px solid #e2e8f0" }}>
                  "{result.transcript}"
                </p>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginTop: 24 }}>
                  <div>
                    <h3 style={{ color: "#1e293b", fontSize: 18, borderBottom: "2px solid #e2e8f0", paddingBottom: 8 }}>🎙️ Delivery</h3>
                    <ul style={{ color: "#475569", paddingLeft: 20, lineHeight: 1.8 }}>
                      <li><strong>Speaking rate:</strong> {result.delivery.words_per_minute?.toFixed(0)} wpm</li>
                      <li><strong>Filler words:</strong> {result.delivery.filler_word_count}</li>
                      <li><strong>Pauses:</strong> {result.delivery.pause_count} (longest {result.delivery.longest_pause_seconds?.toFixed(1)}s)</li>
                    </ul>
                  </div>

                  <div>
                    <h3 style={{ color: "#1e293b", fontSize: 18, borderBottom: "2px solid #e2e8f0", paddingBottom: 8 }}>🧠 Content</h3>
                    <ul style={{ color: "#475569", paddingLeft: 20, lineHeight: 1.8 }}>
                      <li><strong>Relevance:</strong> {result.content.relevance_score}/10</li>
                      <li><strong>Completeness:</strong> {result.content.completeness_score}/10</li>
                      <li><strong>Structure:</strong> {result.content.structure_score}/10</li>
                    </ul>
                  </div>
                </div>

                {(result.content.strengths?.length > 0 || result.content.improvements?.length > 0) && (
                  <div style={{ marginTop: 24 }}>
                    <h3 style={{ color: "#1e293b", fontSize: 18, borderBottom: "2px solid #e2e8f0", paddingBottom: 8 }}>💡 Feedback</h3>
                    
                    {result.content.strengths?.length > 0 && (
                      <div style={{ marginBottom: 12 }}>
                        <strong style={{ color: "#16a34a" }}>Strengths:</strong>
                        <ul style={{ color: "#475569", margin: "4px 0 0 0", paddingLeft: 20 }}>
                          {result.content.strengths.map((s, i) => <li key={i}>{s}</li>)}
                        </ul>
                      </div>
                    )}
                    
                    {result.content.improvements?.length > 0 && (
                      <div>
                        <strong style={{ color: "#ea580c" }}>To Improve:</strong>
                        <ul style={{ color: "#475569", margin: "4px 0 0 0", paddingLeft: 20 }}>
                          {result.content.improvements.map((s, i) => <li key={i}>{s}</li>)}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {result?.error && (
              <div style={{
                color: "#b91c1c",
                background: "#fef2f2",
                padding: 16,
                borderRadius: 8,
                border: "1px solid #fca5a5",
                marginTop: 24
              }}>
                <strong>Error:</strong> {result.error}
              </div>
            )}
          </div>
        ) : (
          <Dashboard />
        )}
      </div>
      
      <style>{`
        @keyframes pulse {
          0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
          70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
          100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
      `}</style>
    </div>
  );
}
