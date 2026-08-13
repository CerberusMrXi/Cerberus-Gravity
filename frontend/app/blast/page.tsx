"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { FullAnalysis, BlastRadius } from "@/types";
import { Panel } from "@/components/ui/Panel";
import { StatCard } from "@/components/ui/StatCard";
import { Loader2, Bomb } from "lucide-react";

export default function BlastPage() {
  const [data, setData] = useState<FullAnalysis | null>(null);
  const [blast, setBlast] = useState<BlastRadius | null>(null);
  const [nodeId, setNodeId] = useState("id-admin");
  const [loading, setLoading] = useState(true);
  const [computing, setComputing] = useState(false);

  useEffect(() => {
    api.fullAnalysis().then((d) => {
      setData(d);
      setLoading(false);
    });
  }, []);

  const run = async (id: string) => {
    setNodeId(id);
    setComputing(true);
    try {
      const r = await api.blast(id);
      setBlast(r);
    } finally {
      setComputing(false);
    }
  };

  useEffect(() => {
    if (data) run("id-admin");
  }, [data]);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-screen text-slate-400 gap-2">
        <Loader2 className="animate-spin" size={18} /> Loading…
      </div>
    );
  }

  const assets = data.top_gravity_assets;

  return (
    <div className="p-6 space-y-6 max-w-5xl">
      <header>
        <h1 className="text-xl font-semibold flex items-center gap-2">
          <Bomb size={20} className="text-red-400" /> Blast Radius
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          What happens to the attack graph if this node becomes compromised?
        </p>
      </header>

      <div className="flex flex-wrap gap-2">
        {assets.map((a) => (
          <button
            key={a.id}
            onClick={() => run(a.id)}
            className={`px-3 py-1.5 rounded-md text-xs border transition-colors ${
              nodeId === a.id
                ? "border-red-500/50 bg-red-950/30 text-red-300"
                : "border-cerberus-border text-slate-400 hover:bg-slate-800"
            }`}
          >
            {a.name}
          </button>
        ))}
      </div>

      {computing && (
        <div className="text-sm text-slate-400 flex items-center gap-2">
          <Loader2 className="animate-spin" size={14} /> Computing…
        </div>
      )}

      {blast && !computing && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <StatCard label="Blast Score" value={blast.blast_score} accent="red" />
            <StatCard label="Reachable" value={blast.reachable_count} accent="amber" />
            <StatCard label="High Privilege" value={blast.high_privilege_exposed.length} accent="violet" />
            <StatCard label="Critical Exposed" value={blast.critical_assets_exposed.length} accent="red" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Panel title="Critical Assets Exposed">
              <ul className="space-y-2 text-sm">
                {blast.critical_assets_exposed.map((c) => (
                  <li key={c.id} className="flex justify-between">
                    <span>{c.name}</span>
                    <span className="font-mono text-slate-400">g={c.gravity}</span>
                  </li>
                ))}
                {blast.critical_assets_exposed.length === 0 && (
                  <li className="text-slate-500">None</li>
                )}
              </ul>
            </Panel>
            <Panel title="High Privilege Exposed">
              <ul className="space-y-2 text-sm">
                {blast.high_privilege_exposed.map((c) => (
                  <li key={c.id} className="flex justify-between">
                    <span>{c.name}</span>
                    <span className="font-mono text-slate-400">priv={c.privilege}</span>
                  </li>
                ))}
                {blast.high_privilege_exposed.length === 0 && (
                  <li className="text-slate-500">None</li>
                )}
              </ul>
            </Panel>
          </div>
        </>
      )}
    </div>
  );
}
