"use client";

import { useQuery } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/store/auth";
import { crmApi } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

const stageColors: Record<string, "default" | "success" | "warning" | "destructive" | "secondary"> = {
  new: "secondary", contacted: "default", qualified: "warning",
  proposal: "default", negotiation: "warning", won: "success", lost: "destructive",
};

export default function OpportunitiesPage() {
  const { tokens, organization } = useAuthStore();

  const { data, isLoading } = useQuery({
    queryKey: ["opportunities"],
    queryFn: () => crmApi.getOpportunities(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  return (
    <>
      <DashboardHeader title="Opportunities" />
      <div className="flex-1 overflow-y-auto p-6">
        {isLoading ? (
          <div className="flex h-32 items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 dark:bg-slate-900">
                <tr>
                  <th className="px-4 py-3 text-left font-medium">Title</th>
                  <th className="px-4 py-3 text-left font-medium">Customer</th>
                  <th className="px-4 py-3 text-left font-medium">Stage</th>
                  <th className="px-4 py-3 text-left font-medium">Amount</th>
                  <th className="px-4 py-3 text-left font-medium">Probability</th>
                  <th className="px-4 py-3 text-left font-medium">Close Date</th>
                </tr>
              </thead>
              <tbody>
                {data?.results.map((opp) => (
                  <tr key={opp.id} className="border-t border-slate-100 dark:border-slate-800">
                    <td className="px-4 py-3 font-medium">{opp.title}</td>
                    <td className="px-4 py-3">{opp.customer_name || "—"}</td>
                    <td className="px-4 py-3"><Badge variant={stageColors[opp.stage]}>{opp.stage}</Badge></td>
                    <td className="px-4 py-3">{formatCurrency(parseFloat(opp.amount))}</td>
                    <td className="px-4 py-3">{opp.probability}%</td>
                    <td className="px-4 py-3">{opp.expected_close_date ? formatDate(opp.expected_close_date) : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
