"use client";

import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuthStore } from "@/store/auth";

export default function SettingsPage() {
  const { user, organization } = useAuthStore();

  return (
    <>
      <DashboardHeader title="Settings" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-2xl">
        <Card>
          <CardHeader><CardTitle>Profile</CardTitle></CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="flex justify-between"><span className="text-slate-500">Name</span><span>{user?.full_name}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Email</span><span>{user?.email}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Role</span><span className="capitalize">{user?.role?.replace("_", " ")}</span></div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Organization</CardTitle></CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="flex justify-between"><span className="text-slate-500">Name</span><span>{organization?.name}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Plan</span><span className="capitalize">{organization?.plan}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Slug</span><span>{organization?.slug}</span></div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
