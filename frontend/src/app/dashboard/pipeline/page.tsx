"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/store/auth";
import { crmApi } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

const STAGES = ["new", "contacted", "qualified", "proposal", "negotiation", "won", "lost"];

export default function PipelinePage() {
  const { tokens, organization } = useAuthStore();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["pipeline"],
    queryFn: () => crmApi.getPipeline(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  const moveMutation = useMutation({
    mutationFn: ({ id, stage }: { id: string; stage: string }) =>
      crmApi.updateOpportunityStage(tokens!.access, organization!.id, id, stage),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["pipeline"] }),
  });

  const handleDragStart = (e: React.DragEvent, oppId: string) => {
    e.dataTransfer.setData("oppId", oppId);
  };

  const handleDrop = (e: React.DragEvent, stage: string) => {
    e.preventDefault();
    const oppId = e.dataTransfer.getData("oppId");
    if (oppId) moveMutation.mutate({ id: oppId, stage });
  };

  return (
    <>
      <DashboardHeader title="Sales Pipeline" />
      <div className="flex-1 overflow-x-auto p-6">
        {isLoading ? (
          <div className="flex h-32 items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          </div>
        ) : (
          <div className="flex gap-4 min-w-max">
            {STAGES.map((stage) => {
              const col = data?.[stage];
              return (
                <div
                  key={stage}
                  className="w-72 flex-shrink-0 rounded-xl bg-slate-100 p-3 dark:bg-slate-800"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => handleDrop(e, stage)}
                >
                  <div className="mb-3 flex items-center justify-between">
                    <h3 className="text-sm font-semibold capitalize">{stage}</h3>
                    <Badge variant="secondary">{col?.count || 0}</Badge>
                  </div>
                  <p className="mb-3 text-xs text-slate-500">{formatCurrency(col?.total_amount || 0)}</p>
                  <div className="space-y-2">
                    {col?.opportunities.map((opp) => (
                      <div
                        key={opp.id}
                        draggable
                        onDragStart={(e) => handleDragStart(e, opp.id)}
                        className="cursor-grab rounded-lg border border-slate-200 bg-white p-3 shadow-sm active:cursor-grabbing dark:border-slate-700 dark:bg-slate-900"
                      >
                        <p className="text-sm font-medium">{opp.title}</p>
                        <p className="mt-1 text-xs text-slate-500">{formatCurrency(parseFloat(opp.amount))}</p>
                        <p className="text-xs text-slate-400">{opp.probability}% probability</p>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
}
