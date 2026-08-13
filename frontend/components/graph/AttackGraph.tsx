"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  MarkerType,
  Position,
  useNodesState,
  useEdgesState,
  Handle,
  NodeProps,
} from "reactflow";
import "reactflow/dist/style.css";
import type { AssetNode, GraphEdge, AttackPath } from "@/types";
import { gravityColor, gravityLabel } from "@/lib/api";
import { cn } from "@/lib/utils";

interface AttackGraphProps {
  nodes: AssetNode[];
  edges: GraphEdge[];
  gravityMap?: Record<string, number>;
  wells?: string[];
  highlightedPath?: string[];
  selectedNodeId?: string | null;
  onNodeSelect?: (id: string) => void;
}

function AssetNodeView({ data }: NodeProps) {
  const g = data.gravity ?? 0;
  const isWell = data.isWell;
  const isHighlight = data.isHighlight;
  const isSelected = data.isSelected;

  return (
    <div
      className={cn(
        "px-3 py-2 rounded-md border min-w-[120px] max-w-[160px] shadow-lg transition-all",
        isSelected && "ring-2 ring-blue-400",
        isHighlight && "ring-2 ring-amber-400",
        isWell ? "border-pink-500/70 bg-pink-950/40" : "border-slate-600 bg-slate-900/90"
      )}
      style={{
        borderColor: isWell ? undefined : gravityColor(g) + "99",
        boxShadow: isWell ? "0 0 12px rgba(236,72,153,0.35)" : undefined,
      }}
    >
      <Handle type="target" position={Position.Top} className="!bg-slate-500 !w-2 !h-2" />
      <div className="flex items-center justify-between gap-2">
        <span className="text-[10px] uppercase tracking-wide text-slate-400 truncate">
          {data.type || "asset"}
        </span>
        <span
          className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded"
          style={{ background: gravityColor(g) + "33", color: gravityColor(g) }}
        >
          {g.toFixed(0)}
        </span>
      </div>
      <div className="mt-1 text-xs font-medium text-slate-100 truncate" title={data.label}>
        {data.label}
      </div>
      {isWell && (
        <div className="mt-1 text-[9px] text-pink-400 uppercase tracking-wider">Gravity Well</div>
      )}
      <Handle type="source" position={Position.Bottom} className="!bg-slate-500 !w-2 !h-2" />
    </div>
  );
}

const nodeTypes = { asset: AssetNodeView };

function layoutNodes(nodes: AssetNode[]): Node[] {
  // Simple layered layout by approximate tier from demo topology
  const tiers: Record<string, number> = {
    "inet-01": 0,
    "web-01": 1,
    "mail-01": 1,
    "app-01": 2,
    "ws-01": 2,
    "jump-01": 3,
    "file-01": 3,
    "id-admin": 3,
    "db-01": 4,
    "crit-01": 4,
  };

  const byTier: Record<number, AssetNode[]> = {};
  nodes.forEach((n) => {
    const t = tiers[n.id] ?? 2;
    if (!byTier[t]) byTier[t] = [];
    byTier[t].push(n);
  });

  const result: Node[] = [];
  Object.entries(byTier).forEach(([tierStr, list]) => {
    const tier = Number(tierStr);
    const y = 40 + tier * 140;
    const spacing = 180;
    const startX = 80;
    list.forEach((n, i) => {
      result.push({
        id: n.id,
        type: "asset",
        position: { x: startX + i * spacing, y },
        data: {
          label: n.name || n.id,
          type: n.type,
          gravity: n.gravity ?? 0,
          isWell: false,
          isHighlight: false,
          isSelected: false,
        },
      });
    });
  });
  return result;
}

export function AttackGraph({
  nodes,
  edges,
  gravityMap = {},
  wells = [],
  highlightedPath = [],
  selectedNodeId,
  onNodeSelect,
}: AttackGraphProps) {
  const wellSet = useMemo(() => new Set(wells), [wells]);
  const pathSet = useMemo(() => new Set(highlightedPath), [highlightedPath]);

  const initialNodes = useMemo(() => {
    const laid = layoutNodes(nodes);
    return laid.map((n) => ({
      ...n,
      data: {
        ...n.data,
        gravity: gravityMap[n.id] ?? n.data.gravity ?? 0,
        isWell: wellSet.has(n.id),
        isHighlight: pathSet.has(n.id),
        isSelected: selectedNodeId === n.id,
      },
    }));
  }, [nodes, gravityMap, wellSet, pathSet, selectedNodeId]);

  const initialEdges = useMemo((): Edge[] => {
    return edges.map((e, i) => {
      const onPath =
        highlightedPath.length > 1 &&
        highlightedPath.some(
          (id, idx) =>
            idx < highlightedPath.length - 1 &&
            highlightedPath[idx] === e.source &&
            highlightedPath[idx + 1] === e.target
        );
      return {
        id: `e-${e.source}-${e.target}-${i}`,
        source: e.source,
        target: e.target,
        label: e.relationship_type || "",
        animated: onPath,
        style: {
          stroke: onPath ? "#f59e0b" : "#475569",
          strokeWidth: onPath ? 2.5 : 1.5,
        },
        labelStyle: { fill: "#94a3b8", fontSize: 9 },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: onPath ? "#f59e0b" : "#475569",
          width: 16,
          height: 16,
        },
      };
    });
  }, [edges, highlightedPath]);

  const [rfNodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [rfEdges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  useEffect(() => {
    setEdges(initialEdges);
  }, [initialEdges, setEdges]);

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      onNodeSelect?.(node.id);
    },
    [onNodeSelect]
  );

  return (
    <div className="w-full h-full min-h-[480px] rounded-lg border border-cerberus-border overflow-hidden">
      <ReactFlow
        nodes={rfNodes}
        edges={rfEdges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.3}
        maxZoom={1.8}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1e293b" gap={20} size={1} />
        <Controls showInteractive={false} />
        <MiniMap
          nodeColor={(n) => gravityColor(n.data?.gravity ?? 0)}
          maskColor="rgba(10,14,23,0.7)"
        />
      </ReactFlow>
    </div>
  );
}
