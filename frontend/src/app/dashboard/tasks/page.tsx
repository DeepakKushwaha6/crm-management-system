"use client";

import { useQuery } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/store/auth";
import { crmApi } from "@/lib/api";
import { formatDate } from "@/lib/utils";

const priorityVariant = (p: string) => {
  const map: Record<string, "default" | "success" | "warning" | "destructive"> = {
    low: "success", medium: "default", high: "warning", urgent: "destructive",
  };
  return map[p] || "default";
};

export default function TasksPage() {
  const { tokens, organization } = useAuthStore();

  const { data, isLoading } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => crmApi.getTasks(tokens!.access, organization!.id),
    enabled: !!tokens && !!organization,
  });

  return (
    <>
      <DashboardHeader title="Tasks" />
      <div className="flex-1 overflow-y-auto p-6">
        {isLoading ? (
          <div className="flex h-32 items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          </div>
        ) : (
          <div className="space-y-3">
            {data?.results.map((task) => (
              <div key={task.id} className="flex items-center justify-between rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <div>
                  <h3 className="font-medium">{task.title}</h3>
                  <p className="text-sm text-slate-500">{task.description}</p>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={priorityVariant(task.priority)}>{task.priority}</Badge>
                  <Badge variant={task.status === "completed" ? "success" : "secondary"}>{task.status}</Badge>
                  {task.due_date && <span className="text-xs text-slate-400">{formatDate(task.due_date)}</span>}
                </div>
              </div>
            ))}
            {data?.results.length === 0 && (
              <p className="text-center text-slate-500 py-8">No tasks yet.</p>
            )}
          </div>
        )}
      </div>
    </>
  );
}
