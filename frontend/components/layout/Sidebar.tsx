"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, ListFilter, Activity, Gavel, Settings, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";
import { useUIStore } from "@/store/ui-store";

const routes = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Transactions", href: "/transactions", icon: ListFilter },
  { name: "Monitoring", href: "/monitoring", icon: Activity },
  { name: "Rules Engine", href: "/rules", icon: Gavel },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { sidebarOpen } = useUIStore();

  if (!sidebarOpen) return null;

  return (
    <div className="w-64 h-screen border-r bg-zinc-950 text-zinc-300 flex flex-col sticky left-0 top-0 z-30">
      <div className="h-14 flex items-center px-4 border-b border-zinc-800">
        <ShieldAlert className="w-5 h-5 text-indigo-500 mr-2" />
        <span className="font-semibold text-white tracking-tight">FinTech-1 Ops</span>
      </div>
      <div className="p-4 flex-1 space-y-1">
        {routes.map((route) => (
          <Link
            key={route.href}
            href={route.href}
            className={cn(
              "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
              pathname.startsWith(route.href)
                ? "bg-indigo-500/10 text-indigo-400"
                : "hover:bg-zinc-900 hover:text-white"
            )}
          >
            <route.icon className="w-4 h-4 mr-3" />
            {route.name}
          </Link>
        ))}
      </div>
      <div className="p-4 text-xs text-zinc-600">
        v2.0 (Next.js Edge)
      </div>
    </div>
  );
}
