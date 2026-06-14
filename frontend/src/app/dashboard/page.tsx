"use client";

import { useQuery } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { DashboardKPIs } from "@/components/dashboard/kpi-cards";
import { RevenueChart, FunnelChartWidget } from "@/components/dashboard/charts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuthStore } from "@/store/auth";
import { crmApi } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function DashboardPage() {
  const { tokens, organization } = useAuthStore();

  const { data: dashboard, isLoading } = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => crmApi.getDashboard(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  const { data: revenue } = useQuery({
    queryKey: ["revenue-analytics"],
    queryFn: () => crmApi.getRevenueAnalytics(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  const { data: pipeline } = useQuery({
    queryKey: ["pipeline-analytics"],
    queryFn: () => crmApi.getPipelineAnalytics(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  return (
    <>
      <DashboardHeader title="Dashboard" />
      <div className="flex-1 overflow-y-auto p-6">
        {isLoading ? (
          <div className="flex h-64 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
          </div>
        ) : dashboard ? (
          <div className="space-y-6">
            <DashboardKPIs
              revenue={dashboard.revenue}
              sales={dashboard.sales}
              conversion={dashboard.conversion}
              customers={dashboard.customers}
              tasks={dashboard.tasks}
            />
            <div className="grid gap-6 lg:grid-cols-2">
              {revenue && <RevenueChart data={revenue.data} />}
              {pipeline && <FunnelChartWidget data={pipeline.funnel} />}
            </div>
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {dashboard.recent_activities.length === 0 ? (
                    <p className="text-sm text-slate-500">No recent activities</p>
                  ) : (
                    dashboard.recent_activities.map((a) => (
                      <div key={a.id} className="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0 dark:border-slate-800">
                        <div>
                          <p className="text-sm font-medium">{a.subject}</p>
                          <p className="text-xs text-slate-500">{a.user__email} · {a.activity_type}</p>
                        </div>
                        <span className="text-xs text-slate-400">{formatDate(a.created_at)}</span>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        ) : null}
      </div>
    </>
  );
}
