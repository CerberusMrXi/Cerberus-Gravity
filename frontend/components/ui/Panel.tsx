import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface PanelProps {
  title?: string;
  children: ReactNode;
  className?: string;
  action?: ReactNode;
}

export function Panel({ title, children, className, action }: PanelProps) {
  return (
    <div className={cn("rounded-lg border border-cerberus-border bg-cerberus-panel overflow-hidden", className)}>
      {title && (
        <div className="flex items-center justify-between px-4 py-3 border-b border-cerberus-border">
          <h3 className="text-sm font-medium text-slate-200">{title}</h3>
          {action}
        </div>
      )}
      <div className="p-4">{children}</div>
    </div>
  );
}
