"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { TrendingUp, TrendingDown, Users, Target, DollarSign, CheckCircle } from "lucide-react";

interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: React.ReactNode;
}

export function KPICard({ title, value, change, icon }: KPICardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-slate-500">{title}</CardTitle>
        <div className="rounded-lg bg-blue-50 p-2 text-blue-600 dark:bg-blue-950 dark:text-blue-400">
          {icon}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change !== undefined && (
          <p className={`mt-1 flex items-center text-xs ${change >= 0 ? "text-green-600" : "text-red-600"}`}>
            {change >= 0 ? <TrendingUp className="mr-1 h-3 w-3" /> : <TrendingDown className="mr-1 h-3 w-3" />}
            {Math.abs(change)}% from last month
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export function DashboardKPIs({
  revenue,
  sales,
  conversion,
  customers,
  tasks,
}: {
  revenue: { total: number; monthly: number; pipeline_value: number };
  sales: { total_leads: number; open_opportunities: number; won_deals: number };
  conversion: { lead_conversion_rate: number; win_rate: number };
  customers: { total: number; active: number; at_risk: number };
  tasks: { pending: number; overdue: number };
}) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <KPICard title="Total Revenue" value={formatCurrency(revenue.total)} change={12} icon={<DollarSign className="h-4 w-4" />} />
      <KPICard title="Monthly Revenue" value={formatCurrency(revenue.monthly)} change={8} icon={<TrendingUp className="h-4 w-4" />} />
      <KPICard title="Pipeline Value" value={formatCurrency(revenue.pipeline_value)} icon={<Target className="h-4 w-4" />} />
      <KPICard title="Total Leads" value={sales.total_leads} change={5} icon={<Users className="h-4 w-4" />} />
      <KPICard title="Open Deals" value={sales.open_opportunities} icon={<Target className="h-4 w-4" />} />
      <KPICard title="Win Rate" value={`${conversion.win_rate}%`} icon={<CheckCircle className="h-4 w-4" />} />
      <KPICard title="Active Customers" value={customers.active} icon={<Users className="h-4 w-4" />} />
      <KPICard title="Pending Tasks" value={tasks.pending} icon={<CheckCircle className="h-4 w-4" />} />
    </div>
  );
}
