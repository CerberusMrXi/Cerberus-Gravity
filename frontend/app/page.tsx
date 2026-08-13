"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { FullAnalysis } from "@/types";
import { StatCard } from "@/components/ui/StatCard";
import { Panel } from "@/components/ui/Panel";
import { GravityDistribution } from "@/components/dashboard/GravityDistribution";
import { TopAssets } from "@/components/dashboard/TopAssets";
import { PathList } from "@/components/dashboard/PathList";
import { AttackGraph } from "@/components/graph/AttackGraph";
import {
  Network,
  Gauge,
  ShieldAlert,
  Waves,
  Activity,
  Loader2,
  AlertCircle,
} from "lucide-react";

export default function DashboardPage() {
  const [data, setData] = useState<FullAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedPath, setSelectedPath] = useState(0);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  useEffect(() => {
    api
      .fullAnalysis()
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message || "Failed to load analysis. Is the backend running on :8000?");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-slate-400 gap-2">
        <Loader2 className="animate-spin" size={20} />
        Loading CERBERUS analysis…
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex flex-col items-center justify-center h-screen text-slate-400 gap-3 px-6">
        <AlertCircle size={32} className="text-amber-500" />
        <p className="text-center max-w-md">{error}</p>
        <p className="text-xs text-slate-500">
          Start backend: <code className="bg-slate-800 px-1.5 py-0.5 rounded">cd backend && PYTHONPATH=. python -m uvicorn app.main:app --port 8000</code>
        </p>
      </div>
    );
  }

  const wells = [
    ...(data.gravity_wells.single_node_wells.flatMap((w) => w.nodes) || []),
    ...(data.gravity_wells.multi_node_wells.flatMap((w) => w.nodes) || []),
  ];

  const nameMap: Record<string, string> = {};
  data.graph.nodes.forEach((n) => {
    nameMap[n.id] = n.name || n.id;
  });

  const pathNodes = data.attack_paths[selectedPath]?.nodes || [];

  return (
    <div className="p-6 space-y-6 max-w-[1600px]">
      <header className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-slate-100">Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            {data.dataset} · Experimental gravity model
          </p>
        </div>
        <div className="text-[10px] text-slate-600 max-w-xs text-right leading-relaxed">
          Metrics are research constructs, not industry standards.
        </div>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <StatCard label="Attack Surface" value={data.metrics.node_count} sub={`${data.metrics.edge_count} edges`} icon={Network} accent="blue" />
        <StatCard label="Gravity Score" value={data.top_gravity_assets[0]?.gravity.toFixed(0) ?? "—"} sub="Peak asset" icon={Gauge} accent="violet" />
        <StatCard label="Critical Assets" value={data.gravity_distribution.CRITICAL + data.gravity_distribution.VERY_HIGH} sub="≥60 gravity" icon={ShieldAlert} accent="red" />
        <StatCard label="High-Risk Paths" value={data.attack_paths.length} sub="To objective" icon={Activity} accent="amber" />
        <StatCard label="Gravity Wells" value={data.gravity_wells.total_wells} sub={`threshold ${data.gravity_wells.threshold}`} icon={Waves} accent="violet" />
        <StatCard label="Concentration" value={data.metrics.gravity_concentration.toFixed(2)} sub="Gini-like" icon={Gauge} accent="green" />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <Panel title="Attack Graph" className="xl:col-span-2">
          <div className="h-[420px]">
            <AttackGraph
              nodes={data.graph.nodes}
              edges={data.graph.edges}
              gravityMap={data.gravity_map}
              wells={wells}
              highlightedPath={pathNodes}
              selectedNodeId={selectedNode}
              onNodeSelect={setSelectedNode}
            />
          </div>
        </Panel>

        <div className="space-y-4">
          <Panel title="Gravity Distribution">
            <GravityDistribution distribution={data.gravity_distribution} />
          </Panel>
          <Panel title="Top Gravity Assets">
            <TopAssets assets={data.top_gravity_assets} onSelect={setSelectedNode} />
          </Panel>
        </div>
      </div>

      <Panel title="Top Attack Paths">
        <PathList
          paths={data.attack_paths}
          selectedIndex={selectedPath}
          onSelect={setSelectedPath}
          nameMap={nameMap}
        />
      </Panel>
    </div>
  );
}
