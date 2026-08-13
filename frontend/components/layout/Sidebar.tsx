"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Network,
  Shield,
  FlaskConical,
  Settings,
  Activity,
  Bomb,
} from "lucide-react";
import { cn } from "@/lib/utils";

const nav = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/graph", label: "Attack Graph", icon: Network },
  { href: "/paths", label: "Attack Paths", icon: Activity },
  { href: "/blast", label: "Blast Radius", icon: Bomb },
  { href: "/research", label: "Research Mode", icon: FlaskConical },
  { href: "/remediate", label: "Remediation", icon: Shield },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 shrink-0 border-r border-cerberus-border bg-cerberus-panel flex flex-col h-screen sticky top-0">
      <div className="px-4 py-5 border-b border-cerberus-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-600 to-blue-600 flex items-center justify-center text-sm font-bold">
            CG
          </div>
          <div>
            <div className="font-semibold text-sm tracking-wide">CERBERUS</div>
            <div className="text-[10px] text-cerberus-muted uppercase tracking-wider">Gravity</div>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-0.5">
        {nav.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors",
                active
                  ? "bg-blue-600/20 text-blue-400 border border-blue-600/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              )}
            >
              <Icon size={16} strokeWidth={1.75} />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="p-3 border-t border-cerberus-border text-[10px] text-cerberus-muted space-y-1">
        <div>Experimental research model</div>
        <div>© 2026 Sudeepa Wanigarathna</div>
      </div>
    </aside>
  );
}
