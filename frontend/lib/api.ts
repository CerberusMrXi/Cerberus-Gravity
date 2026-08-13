import type { FullAnalysis, BlastRadius, RemediationResult } from "@/types";

const BASE =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
    : process.env.BACKEND_URL || "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text || res.statusText}`);
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string; project: string; nodes?: number }>("/api/v1/analysis/health"),

  fullAnalysis: (entry?: string, objective?: string, mode = "strategic") => {
    const params = new URLSearchParams({ mode });
    if (entry) params.set("entry", entry);
    if (objective) params.set("objective", objective);
    return request<FullAnalysis>(`/api/v1/analysis/full?${params}`);
  },

  gravity: () => request<{ gravity_map: Record<string, number> }>("/api/v1/analysis/gravity"),

  blast: (nodeId: string) => request<BlastRadius>(`/api/v1/analysis/blast/${nodeId}`),

  remediate: (nodeId: string, action: string) =>
    request<RemediationResult>("/api/v1/analysis/remediate", {
      method: "POST",
      body: JSON.stringify({ node_id: nodeId, action }),
    }),

  updateWeights: (weights: Record<string, number>) =>
    request<{ message: string; weights: Record<string, number> }>("/api/v1/analysis/weights", {
      method: "POST",
      body: JSON.stringify(weights),
    }),

  graph: () => request<{ nodes: unknown[]; edges: unknown[] }>("/api/v1/graph/"),

  datasets: () => request<{ datasets: string[] }>("/api/v1/analysis/datasets"),

  loadDataset: (name: string) =>
    request<{ name: string; nodes: number; edges: number }>(`/api/v1/analysis/load/${name}`, {
      method: "POST",
    }),
};

export function gravityColor(g: number): string {
  if (g >= 80) return "#ef4444";
  if (g >= 60) return "#f59e0b";
  if (g >= 40) return "#3b82f6";
  if (g >= 20) return "#22c55e";
  return "#64748b";
}

export function gravityLabel(g: number): string {
  if (g >= 80) return "CRITICAL";
  if (g >= 60) return "VERY HIGH";
  if (g >= 40) return "HIGH";
  if (g >= 20) return "MODERATE";
  return "LOW";
}
