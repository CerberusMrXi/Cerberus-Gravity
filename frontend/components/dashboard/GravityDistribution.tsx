"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const COLORS: Record<string, string> = {
  LOW: "#64748b",
  MODERATE: "#22c55e",
  HIGH: "#3b82f6",
  VERY_HIGH: "#f59e0b",
  CRITICAL: "#ef4444",
};

interface Props {
  distribution: Record<string, number>;
}

export function GravityDistribution({ distribution }: Props) {
  const data = ["LOW", "MODERATE", "HIGH", "VERY_HIGH", "CRITICAL"].map((k) => ({
    name: k.replace("_", " "),
    count: distribution[k] ?? 0,
    key: k,
  }));

  return (
    <div className="h-48">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
          <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 10 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} allowDecimals={false} />
          <Tooltip
            contentStyle={{ background: "#111827", border: "1px solid #1e293b", borderRadius: 8, fontSize: 12 }}
            labelStyle={{ color: "#e2e8f0" }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((d) => (
              <Cell key={d.key} fill={COLORS[d.key]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
