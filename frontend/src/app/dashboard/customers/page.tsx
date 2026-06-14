"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/store/auth";
import { crmApi, aiApi } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { Brain } from "lucide-react";

export default function CustomersPage() {
  const { tokens, organization } = useAuthStore();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["customers"],
    queryFn: () => crmApi.getCustomers(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  const churnMutation = useMutation({
    mutationFn: (id: string) => aiApi.predictChurn(tokens!.access, organization!.id, id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["customers"] }),
  });

  return (
    <>
      <DashboardHeader title="Customers" />
      <div className="flex-1 overflow-y-auto p-6">
        {isLoading ? (
          <div className="flex h-32 items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {data?.results.map((c) => (
              <div key={c.id} className="rounded-xl border border-slate-200 p-6 dark:border-slate-800">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold">{c.name}</h3>
                    <p className="text-sm text-slate-500">{c.company}</p>
                  </div>
                  <Badge variant={c.status === "active" ? "success" : "secondary"}>{c.status}</Badge>
                </div>
                <div className="mt-4 space-y-2 text-sm">
                  <p>LTV: {formatCurrency(parseFloat(c.lifetime_value))}</p>
                  <p>Churn Risk: <span className={c.churn_risk >= 0.7 ? "text-red-600 font-semibold" : "text-green-600"}>{(c.churn_risk * 100).toFixed(0)}%</span></p>
                </div>
                <Button variant="outline" size="sm" className="mt-4 gap-1" onClick={() => churnMutation.mutate(c.id)}>
                  <Brain className="h-3 w-3" /> Predict Churn
                </Button>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
