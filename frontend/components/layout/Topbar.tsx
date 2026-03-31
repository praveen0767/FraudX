"use client";

import { useUIStore } from "@/store/ui-store";
import { Menu, Bell, UserCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Topbar() {
  const { toggleSidebar, sidebarOpen } = useUIStore();

  return (
    <header
      className="h-14 border-b border-zinc-800 bg-zinc-950 flex items-center justify-between px-4 z-10"
    >
      <div className="flex items-center">
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="text-zinc-400 hover:text-white">
          <Menu className="w-5 h-5" />
        </Button>
      </div>
      <div className="flex items-center gap-4 text-zinc-400">
        <Button variant="ghost" size="icon" className="relative hover:text-white">
          <Bell className="w-5 h-5" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
        </Button>
        <Button variant="ghost" size="icon" className="hover:text-white">
          <UserCircle className="w-5 h-5" />
        </Button>
      </div>
    </header>
  );
}
