"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { FullAnalysis } from "@/types";
import { Panel } from "@/components/ui/Panel";
import { PathList } from "@/components/dashboard/PathList";
import { AttackGraph } from "@/components/graph/AttackGraph";
import { Loader2 } from "lucide-react";

export default function PathsPage() {
  const [data, setData] = useState<FullAnalysis | null>(null);
  const [selected, setSelected] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.fullAnalysis().then(setData).finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-screen text-slate-400 gap-2">
        <Loader2 className="animate-spin" size={18} /> Loading paths…
      </div>
    );
  }

  const nameMap: Record<string, string> = {};
  data.graph.nodes.forEach((n) => (nameMap[n.id] = n.name || n.id));
  const path = data.attack_paths[selected];
  const wells = data.gravity_wells.single_node_wells.flatMap((w) => w.nodes);

  return (
    <div className="p-6 space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Attack Paths</h1>
        <p className="text-sm text-slate-500">Ranked by strategic attraction · entry → objective</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Panel title="Paths">
          <PathList paths={data.attack_paths} selectedIndex={selected} onSelect={setSelected} nameMap={nameMap} />
        </Panel>
        <Panel title="Path Detail">
          {!path ? (
            <p className="text-sm text-slate-500">No path selected</p>
          ) : (
            <div className="space-y-3 text-sm">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs text-slate-500">Distance</div>
                  <div className="font-mono text-lg">{path.distance}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">Path Gravity</div>
                  <div className="font-mono text-lg text-violet-400">{path.path_gravity.toFixed(1)}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">Risk</div>
                  <div className="font-mono text-lg text-amber-400">{path.risk.toFixed(1)}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">Strategic Attraction</div>
                  <div className="font-mono text-lg text-blue-400">{path.strategic_attraction.toFixed(1)}</div>
                </div>
              </div>
              <div>
                <div className="text-xs text-slate-500 mb-1">Route</div>
                <div className="text-slate-200 leading-relaxed">
                  {path.nodes.map((n) => nameMap[n] || n).join(" → ")}
                </div>
              </div>
              <div className="text-xs text-slate-500">
                Privilege transitions: {path.privilege_transitions} · Avg trust: {path.average_trust.toFixed(0)} ·
                Efficiency: {path.path_efficiency}
              </div>
            </div>
          )}
        </Panel>
      </div>

      <Panel title="Highlighted Path on Graph">
        <div className="h-[400px]">
          <AttackGraph
            nodes={data.graph.nodes}
            edges={data.graph.edges}
            gravityMap={data.gravity_map}
            wells={wells}
            highlightedPath={path?.nodes || []}
          />
        </div>
      </Panel>
    </div>
  );
}
