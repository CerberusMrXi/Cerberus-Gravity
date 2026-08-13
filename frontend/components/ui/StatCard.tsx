import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  sub?: string;
  icon?: LucideIcon;
  accent?: "blue" | "violet" | "amber" | "red" | "green";
  className?: string;
}

const accents = {
  blue: "from-blue-600/20 to-transparent border-blue-600/30 text-blue-400",
  violet: "from-violet-600/20 to-transparent border-violet-600/30 text-violet-400",
  amber: "from-amber-600/20 to-transparent border-amber-600/30 text-amber-400",
  red: "from-red-600/20 to-transparent border-red-600/30 text-red-400",
  green: "from-emerald-600/20 to-transparent border-emerald-600/30 text-emerald-400",
};

export function StatCard({ label, value, sub, icon: Icon, accent = "blue", className }: StatCardProps) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-gradient-to-b p-4",
        accents[accent],
        "border-cerberus-border bg-cerberus-panel",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="text-[11px] uppercase tracking-wider text-slate-400">{label}</div>
        {Icon && <Icon size={16} className="opacity-70" />}
      </div>
      <div className="mt-2 text-2xl font-semibold tabular-nums tracking-tight text-slate-100">{value}</div>
      {sub && <div className="mt-1 text-xs text-slate-500">{sub}</div>}
    </div>
  );
}
