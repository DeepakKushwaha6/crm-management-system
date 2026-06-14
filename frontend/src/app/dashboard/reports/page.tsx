"use client";

import { useQuery } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { PipelineBarChart } from "@/components/dashboard/charts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuthStore } from "@/store/auth";
import { crmApi } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function ReportsPage() {
  const { tokens, organization } = useAuthStore();

  const { data: pipeline } = useQuery({
    queryKey: ["pipeline-analytics"],
    queryFn: () => crmApi.getPipelineAnalytics(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  const { data: team } = useQuery({
    queryKey: ["team-performance"],
    queryFn: () => crmApi.getTeamPerformance(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  return (
    <>
      <DashboardHeader title="Reports & Analytics" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {pipeline && <PipelineBarChart data={pipeline.funnel} />}
        <Card>
          <CardHeader><CardTitle>Team Performance</CardTitle></CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="py-2 text-left">Name</th>
                    <th className="py-2 text-left">Role</th>
                    <th className="py-2 text-left">Deals Won</th>
                    <th className="py-2 text-left">Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {team?.team.map((m) => (
                    <tr key={m.name} className="border-b border-slate-100 dark:border-slate-800">
                      <td className="py-2">{m.name}</td>
                      <td className="py-2 capitalize">{m.role.replace("_", " ")}</td>
                      <td className="py-2">{m.deals_won}</td>
                      <td className="py-2">{formatCurrency(m.revenue)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
