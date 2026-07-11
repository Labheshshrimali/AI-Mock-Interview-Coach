import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, PieChart, Pie, Cell, Legend } from 'recharts';

const API_BASE = "http://localhost:8080";
const COLORS = ['#3b82f6', '#f59e0b'];

export default function Dashboard() {
  const [data, setData] = useState({ sessions: [], analytics: {} });

  useEffect(() => {
    fetch(`${API_BASE}/sessions`)
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error("Failed to fetch sessions", err));
  }, []);

  const { sessions, analytics } = data;
  const latestSession = sessions[0] || null;

  // Data for LineChart
  const chartData = sessions.map((s, index) => ({
    name: `S${index + 1}`,
    score: (s.scores.relevance_score + s.scores.completeness_score + s.scores.structure_score) / 3 * 10
  })).reverse();

  // Data for RadarChart
  const radarData = latestSession ? [
    { subject: 'Relevance', A: latestSession.scores.relevance_score * 10 },
    { subject: 'Completeness', A: latestSession.scores.completeness_score * 10 },
    { subject: 'Structure', A: latestSession.scores.structure_score * 10 },
  ] : [];

  // Data for PieChart
  const pieData = latestSession ? [
    { name: 'Delivery', value: 40 },
    { name: 'Content', value: 60 },
  ] : [];

  return (
    <div style={{ padding: "20px" }}>
      <h2 style={{ color: "#1e293b", marginBottom: 20 }}>Interview Analytics</h2>
      
      {/* Analytics Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 20 }}>
        {[
          { label: "Average Score", value: analytics.avg_score || 0 },
          { label: "Best Score", value: analytics.best_score || 0 },
          { label: "Total Sessions", value: analytics.total_sessions || 0 },
        ].map((card, i) => (
          <div key={i} style={{ background: "white", padding: 16, borderRadius: 8, border: "1px solid #e2e8f0", textAlign: "center" }}>
            <div style={{ fontSize: 13, color: "#666" }}>{card.label}</div>
            <div style={{ fontSize: 24, fontWeight: 700, color: "#3b82f6" }}>{card.value}</div>
          </div>
        ))}
      </div>
      
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 20 }}>
        {/* Line Chart */}
        <div style={{ height: 300, background: "white", padding: 20, borderRadius: 12, border: "1px solid #e2e8f0" }}>
          <h3 style={{ fontSize: 16, marginBottom: 10 }}>Performance Trend</h3>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Radar Chart */}
        {latestSession && (
          <div style={{ height: 300, background: "white", padding: 20, borderRadius: 12, border: "1px solid #e2e8f0" }}>
            <h3 style={{ fontSize: 16, marginBottom: 10 }}>Latest Content Analysis</h3>
            <ResponsiveContainer width="100%" height="90%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis domain={[0, 100]} />
                <Radar name="Score" dataKey="A" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      <h3 style={{ color: "#1e293b", marginBottom: 15 }}>Session History</h3>
      <div style={{ display: "grid", gap: 16 }}>
        {sessions.map((s) => (
          <div key={s.id} style={{ background: "white", padding: 16, borderRadius: 8, border: "1px solid #e2e8f0" }}>
            <h4 style={{ margin: "0 0 8px 0" }}>{s.question}</h4>
            <p style={{ fontSize: 13, color: "#666" }}>{new Date(s.timestamp).toLocaleString()}</p>
            <div style={{ fontWeight: 600 }}>Score: {((s.scores.relevance_score + s.scores.completeness_score + s.scores.structure_score) / 3 * 10).toFixed(1)}/100</div>
          </div>
        ))}
      </div>
    </div>
  );
}
