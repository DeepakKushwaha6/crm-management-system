"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { useAuthStore } from "@/store/auth";
import { crmApi, aiApi, type Lead } from "@/lib/api";
import { Plus, Brain, Search } from "lucide-react";

const statusVariant = (s: string) => {
  const map: Record<string, "default" | "success" | "warning" | "destructive" | "secondary"> = {
    new: "secondary", contacted: "default", qualified: "warning", converted: "success", lost: "destructive",
  };
  return map[s] || "secondary";
};

export default function LeadsPage() {
  const { tokens, organization } = useAuthStore();
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ first_name: "", last_name: "", email: "", company: "", source: "web" });

  const { data, isLoading } = useQuery({
    queryKey: ["leads", search],
    queryFn: () => crmApi.getLeads(tokens!.access, organization!.id, search ? `search=${search}` : ""),
    enabled: !!tokens && !!organization,
  });

  const createMutation = useMutation({
    mutationFn: (data: Partial<Lead>) => crmApi.createLead(tokens!.access, organization!.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leads"] });
      setShowForm(false);
      setForm({ first_name: "", last_name: "", email: "", company: "", source: "web" });
    },
  });

  const scoreMutation = useMutation({
    mutationFn: (leadId: string) => aiApi.scoreLead(tokens!.access, organization!.id, leadId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["leads"] }),
  });

  return (
    <>
      <DashboardHeader title="Leads" />
      <div className="flex-1 overflow-y-auto p-6">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative max-w-sm flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input className="pl-9" placeholder="Search leads..." value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
          <Button onClick={() => setShowForm(!showForm)} className="gap-2">
            <Plus className="h-4 w-4" /> Add Lead
          </Button>
        </div>

        {showForm && (
          <Card className="mb-6">
            <CardContent className="pt-6">
              <form
                onSubmit={(e) => { e.preventDefault(); createMutation.mutate({ ...form, status: "new" }); }}
                className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
              >
                <Input placeholder="First Name" value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} required />
                <Input placeholder="Last Name" value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
                <Input placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
                <Input placeholder="Company" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
                <Button type="submit" disabled={createMutation.isPending}>Create Lead</Button>
              </form>
            </CardContent>
          </Card>
        )}

        {isLoading ? (
          <div className="flex h-32 items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 dark:bg-slate-900">
                <tr>
                  <th className="px-4 py-3 text-left font-medium">Name</th>
                  <th className="px-4 py-3 text-left font-medium">Company</th>
                  <th className="px-4 py-3 text-left font-medium">Email</th>
                  <th className="px-4 py-3 text-left font-medium">Status</th>
                  <th className="px-4 py-3 text-left font-medium">Score</th>
                  <th className="px-4 py-3 text-left font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {data?.results.map((lead) => (
                  <tr key={lead.id} className="border-t border-slate-100 dark:border-slate-800">
                    <td className="px-4 py-3 font-medium">{lead.full_name}</td>
                    <td className="px-4 py-3">{lead.company}</td>
                    <td className="px-4 py-3">{lead.email}</td>
                    <td className="px-4 py-3"><Badge variant={statusVariant(lead.status)}>{lead.status}</Badge></td>
                    <td className="px-4 py-3">
                      <span className={`font-semibold ${lead.score >= 70 ? "text-green-600" : lead.score >= 40 ? "text-yellow-600" : "text-red-600"}`}>
                        {lead.score}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <Button variant="ghost" size="sm" onClick={() => scoreMutation.mutate(lead.id)} className="gap-1">
                        <Brain className="h-3 w-3" /> Score
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {data?.results.length === 0 && (
              <p className="p-8 text-center text-slate-500">No leads found. Create your first lead above.</p>
            )}
          </div>
        )}
      </div>
    </>
  );
}
