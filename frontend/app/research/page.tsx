"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { Panel } from "@/components/ui/Panel";
import { FlaskConical, Loader2 } from "lucide-react";

const DEFAULTS = {
  asset_value_weight: 1.0,
  privilege_weight: 1.2,
  reachability_weight: 1.0,
  trust_weight: 0.8,
  exposure_weight: 1.1,
};

const BASE = typeof window !== "undefined"
  ? process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
  : "http://127.0.0.1:8000";

export default function ResearchPage() {
  const [weights, setWeights] = useState({ ...DEFAULTS });
  const [result, setResult] = useState<{ message: string; weights: Record<string, number> } | null>(null);
  const [expName, setExpName] = useState("Experiment A");
  const [running, setRunning] = useState(false);
  const [saved, setSaved] = useState<string | null>(null);

  const apply = async () => {
    setRunning(true);
    setSaved(null);
    try {
      const r = await api.updateWeights(weights);
      setResult(r);
    } finally {
      setRunning(false);
    }
  };

  const saveExp = async () => {
    setRunning(true);
    try {
      const res = await fetch(`${BASE}/api/v1/analysis/experiments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: expName,
          configuration: { weights },
          results: result,
        }),
      });
      const data = await res.json();
      setSaved(data.id || "saved");
    } finally {
      setRunning(false);
    }
  };

  const reset = () => setWeights({ ...DEFAULTS });

  return (
    <div className="p-6 space-y-6 max-w-2xl">
      <header>
        <h1 className="text-xl font-semibold flex items-center gap-2">
          <FlaskConical size={20} className="text-violet-400" /> Research Mode
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Modify gravity coefficients and recompute. Experimental research model only.
        </p>
      </header>

      <Panel title="Gravity Weights">
        <div className="space-y-4">
          {(Object.keys(DEFAULTS) as (keyof typeof DEFAULTS)[]).map((key) => (
            <div key={key}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400">{key.replace(/_/g, " ")}</span>
                <span className="font-mono text-slate-300">{weights[key].toFixed(2)}</span>
              </div>
              <input
                type="range"
                min={0.2}
                max={2.5}
                step={0.05}
                value={weights[key]}
                onChange={(e) => setWeights({ ...weights, [key]: parseFloat(e.target.value) })}
                className="w-full accent-violet-500"
              />
            </div>
          ))}

          <div className="flex flex-wrap gap-2 pt-2">
            <button
              onClick={apply}
              disabled={running}
              className="px-4 py-2 rounded-md bg-violet-600 hover:bg-violet-500 text-sm font-medium disabled:opacity-50 flex items-center gap-2"
            >
              {running && <Loader2 size={14} className="animate-spin" />}
              Apply & Recompute
            </button>
            <button onClick={reset} className="px-4 py-2 rounded-md border border-cerberus-border text-sm text-slate-400 hover:bg-slate-800">
              Reset Defaults
            </button>
          </div>
        </div>
      </Panel>

      {result && (
        <Panel title="Result">
          <p className="text-sm text-emerald-400">{result.message}</p>
          <pre className="mt-2 text-xs font-mono text-slate-400 bg-slate-900 p-3 rounded overflow-auto">
            {JSON.stringify(result.weights, null, 2)}
          </pre>
          <div className="mt-3 flex flex-wrap gap-2 items-center">
            <input
              value={expName}
              onChange={(e) => setExpName(e.target.value)}
              className="bg-slate-900 border border-cerberus-border rounded px-2 py-1.5 text-sm"
              placeholder="Experiment name"
            />
            <button
              onClick={saveExp}
              disabled={running}
              className="px-3 py-1.5 rounded-md border border-violet-500/40 text-violet-300 text-sm hover:bg-violet-950/40"
            >
              Save Experiment
            </button>
            {saved && <span className="text-xs text-emerald-500">Saved: {saved}</span>}
          </div>
          <p className="mt-2 text-[11px] text-slate-500">
            Return to Dashboard to see updated gravity scores and paths.
          </p>
        </Panel>
      )}

      <div className="text-[11px] text-slate-600 leading-relaxed border border-cerberus-border rounded-lg p-3">
        Changing weights alters the experimental gravity model. This is not an industry-standard risk metric.
      </div>
    </div>
  );
}
