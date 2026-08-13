"use client";

import { useEffect, useState } from "react";
import { api, gravityColor, gravityLabel } from "@/lib/api";
import type { FullAnalysis } from "@/types";
import { AttackGraph } from "@/components/graph/AttackGraph";
import { Panel } from "@/components/ui/Panel";
import { Loader2 } from "lucide-react";

export default function GraphPage() {
  const [data, setData] = useState<FullAnalysis | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.fullAnalysis().then(setData).finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-screen text-slate-400 gap-2">
        <Loader2 className="animate-spin" size={18} /> Loading graph…
      </div>
    );
  }

  const wells = [
    ...data.gravity_wells.single_node_wells.flatMap((w) => w.nodes),
    ...data.gravity_wells.multi_node_wells.flatMap((w) => w.nodes),
  ];

  const node = selected ? data.graph.nodes.find((n) => n.id === selected) : null;
  const g = selected ? data.gravity_map[selected] ?? 0 : 0;
  const crit = selected ? data.strategic_criticality[selected] : undefined;

  return (
    <div className="p-6 h-screen flex flex-col gap-4">
      <header>
        <h1 className="text-xl font-semibold">Attack Graph</h1>
        <p className="text-sm text-slate-500">Interactive view · click a node for details</p>
      </header>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-4 min-h-0">
        <div className="lg:col-span-3 min-h-[500px]">
          <AttackGraph
            nodes={data.graph.nodes}
            edges={data.graph.edges}
            gravityMap={data.gravity_map}
            wells={wells}
            selectedNodeId={selected}
            onNodeSelect={setSelected}
          />
        </div>

        <Panel title="Node Detail" className="overflow-auto">
          {!node ? (
            <p className="text-sm text-slate-500">Select a node</p>
          ) : (
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-slate-400 text-xs uppercase">Name</div>
                <div className="text-slate-100 font-medium">{node.name}</div>
              </div>
              <div>
                <div className="text-slate-400 text-xs uppercase">Type</div>
                <div>{node.type || "—"}</div>
              </div>
              <div>
                <div className="text-slate-400 text-xs uppercase">Gravity</div>
                <div className="flex items-center gap-2">
                  <span className="text-lg font-mono font-semibold" style={{ color: gravityColor(g) }}>
                    {g.toFixed(1)}
                  </span>
                  <span className="text-xs text-slate-500">{gravityLabel(g)}</span>
                </div>
              </div>
              {crit !== undefined && (
                <div>
                  <div className="text-slate-400 text-xs uppercase">Strategic Criticality</div>
                  <div className="font-mono">{crit.toFixed(1)}</div>
                </div>
              )}
              <div className="grid grid-cols-2 gap-2 pt-2 border-t border-cerberus-border text-xs">
                <div>
                  <div className="text-slate-500">Privilege</div>
                  <div>{Number(node.privilege_level ?? 0).toFixed(0)}</div>
                </div>
                <div>
                  <div className="text-slate-500">Exposure</div>
                  <div>{Number(node.exposure ?? 0).toFixed(0)}</div>
                </div>
                <div>
                  <div className="text-slate-500">Reachability</div>
                  <div>{Number(node.reachability ?? 0).toFixed(0)}</div>
                </div>
                <div>
                  <div className="text-slate-500">Business Value</div>
                  <div>{Number(node.business_value ?? 0).toFixed(0)}</div>
                </div>
              </div>
              {wells.includes(node.id) && (
                <div className="mt-2 px-2 py-1.5 rounded bg-pink-950/40 border border-pink-500/30 text-pink-300 text-xs">
                  Gravity Well
                </div>
              )}
            </div>
          )}
        </Panel>
      </div>
    </div>
  );
}
