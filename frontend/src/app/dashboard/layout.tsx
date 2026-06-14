"use client";

import { AuthGuard } from "@/components/auth-guard";
import { DashboardSidebar } from "@/components/layout/dashboard-sidebar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthGuard>
      <div className="flex h-screen overflow-hidden bg-slate-50 dark:bg-slate-900">
        <DashboardSidebar />
        <div className="flex flex-1 flex-col overflow-hidden">{children}</div>
      </div>
    </AuthGuard>
  );
}
