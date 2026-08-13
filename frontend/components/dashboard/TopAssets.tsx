"use client";

import { gravityColor, gravityLabel } from "@/lib/api";

interface Props {
  assets: { id: string; name: string; gravity: number }[];
  onSelect?: (id: string) => void;
}

export function TopAssets({ assets, onSelect }: Props) {
  return (
    <div className="space-y-2">
      {assets.map((a, i) => (
        <button
          key={a.id}
          onClick={() => onSelect?.(a.id)}
          className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800/60 transition-colors text-left"
        >
          <span className="text-xs text-slate-500 w-4 tabular-nums">{i + 1}</span>
          <div className="flex-1 min-w-0">
            <div className="text-sm text-slate-200 truncate">{a.name}</div>
            <div className="text-[10px] text-slate-500">{gravityLabel(a.gravity)}</div>
          </div>
          <div
            className="text-sm font-mono font-semibold tabular-nums"
            style={{ color: gravityColor(a.gravity) }}
          >
            {a.gravity.toFixed(1)}
          </div>
        </button>
      ))}
      {assets.length === 0 && (
        <div className="text-sm text-slate-500 py-4 text-center">No data</div>
      )}
    </div>
  );
}
