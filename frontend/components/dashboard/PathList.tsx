"use client";

import type { AttackPath } from "@/types";
import { cn } from "@/lib/utils";

interface Props {
  paths: AttackPath[];
  selectedIndex?: number;
  onSelect?: (index: number) => void;
  nameMap?: Record<string, string>;
}

export function PathList({ paths, selectedIndex, onSelect, nameMap = {} }: Props) {
  return (
    <div className="space-y-2 max-h-[420px] overflow-y-auto">
      {paths.map((p, i) => (
        <button
          key={i}
          onClick={() => onSelect?.(i)}
          className={cn(
            "w-full text-left px-3 py-2.5 rounded-md border transition-colors",
            selectedIndex === i
              ? "border-amber-500/50 bg-amber-950/20"
              : "border-cerberus-border hover:bg-slate-800/40"
          )}
        >
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="text-xs text-slate-400">Path {i + 1}</span>
            <div className="flex gap-3 text-[10px] font-mono">
              <span className="text-slate-400">d={p.distance}</span>
              <span className="text-violet-400">g={p.path_gravity.toFixed(0)}</span>
              <span className="text-amber-400">r={p.risk.toFixed(0)}</span>
              <span className="text-blue-400">s={p.strategic_attraction.toFixed(0)}</span>
            </div>
          </div>
          <div className="text-[11px] text-slate-300 truncate">
            {p.nodes.map((n) => nameMap[n] || n).join(" → ")}
          </div>
        </button>
      ))}
      {paths.length === 0 && (
        <div className="text-sm text-slate-500 py-6 text-center">No paths found</div>
      )}
    </div>
  );
}
