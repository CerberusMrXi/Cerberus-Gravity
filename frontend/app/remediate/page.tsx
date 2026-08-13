"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { FullAnalysis, RemediationResult } from "@/types";
import { Panel } from "@/components/ui/Panel";
import { Loader2, Shield } from "lucide-react";

const ACTIONS = [
  { id: "reduce_privilege", label: "Reduce Privilege" },
  { id: "reduce_exposure", label: "Reduce Exposure" },
  { id: "reduce_criticality", label: "Reduce Criticality" },
  { id: "remove_outbound_trust", label: "Remove Outbound Trust" },
  { id: "increase_segmentation", label: "Increase Segmentation" },
];

export default function RemediatePage() {
  const [data, setData] = useState<FullAnalysis | null>(null);
  const [nodeId, setNodeId] = useState("id-admin");
  const [action, setAction] = useState("reduce_privilege");
  const [result, setResult] = useState<RemediationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    api.fullAnalysis().then((d) => {
      setData(d);
      setLoading(false);
    });
  }, []);

  const run = async () => {
    setRunning(true);
    try {
      const r = await api.remediate(nodeId, action);
      setResult(r);
    } finally {
      setRunning(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-screen text-slate-400 gap-2">
        <Loader2 className="animate-spin" size={18} /> Loading…
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-3xl">
      <header>
        <h1 className="text-xl font-semibold flex items-center gap-2">
          <Shield size={20} className="text-emerald-400" /> Remediation Analyzer
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Modelled estimates based on the graph — not guarantees about real-world security.
        </p>
      </header>

      <Panel title="Configure">
        <div className="space-y-4">
          <div>
            <label className="text-xs text-slate-400 uppercase">Asset</label>
            <select
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="mt-1 w-full bg-slate-900 border border-cerberus-border rounded-md px-3 py-2 text-sm"
            >
              {data.top_gravity_assets.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name} (g={a.gravity.toFixed(1)})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-400 uppercase">Action</label>
            <select
              value={action}
              onChange={(e) => setAction(e.target.value)}
              className="mt-1 w-full bg-slate-900 border border-cerberus-border rounded-md px-3 py-2 text-sm"
            >
              {ACTIONS.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.label}
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={run}
            disabled={running}
            className="px-4 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 text-sm font-medium disabled:opacity-50"
          >
            {running ? "Simulating…" : "Simulate Remediation"}
          </button>
        </div>
      </Panel>

      {result && (
        <Panel title="Before → After">
          <div className="grid grid-cols-3 gap-4 text-center text-sm">
            <div>
              <div className="text-xs text-slate-500 mb-1">Metric</div>
              <div className="space-y-2 text-left text-slate-400">
                <div>Gravity</div>
                <div>Blast Score</div>
                <div>Reachable</div>
                <div>Critical Exposed</div>
              </div>
            </div>
            <div>
              <div className="text-xs text-slate-500 mb-1">Before</div>
              <div className="space-y-2 font-mono">
                <div>{result.before.gravity.toFixed(1)}</div>
                <div>{result.before.blast_score}</div>
                <div>{result.before.reachable_count}</div>
                <div>{result.before.critical_exposed}</div>
              </div>
            </div>
            <div>
              <div className="text-xs text-slate-500 mb-1">After</div>
              <div className="space-y-2 font-mono text-emerald-400">
                <div>
                  {result.after.gravity.toFixed(1)}{" "}
                  <span className="text-xs text-slate-500">({result.changes.gravity_pct}%)</span>
                </div>
                <div>
                  {result.after.blast_score}{" "}
                  <span className="text-xs text-slate-500">({result.changes.blast_score_pct}%)</span>
                </div>
                <div>
                  {result.after.reachable_count}{" "}
                  <span className="text-xs text-slate-500">({result.changes.reachable_pct}%)</span>
                </div>
                <div>{result.after.critical_exposed}</div>
              </div>
            </div>
          </div>
          <p className="mt-4 text-[11px] text-slate-500 border-t border-cerberus-border pt-3">{result.note}</p>
        </Panel>
      )}
    </div>
  );
}
