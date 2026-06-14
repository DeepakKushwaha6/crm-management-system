"use client";

import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar as CalendarIcon } from "lucide-react";

export default function CalendarPage() {
  const days = Array.from({ length: 35 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - date.getDay() + i);
    return date;
  });

  const today = new Date().toDateString();

  return (
    <>
      <DashboardHeader title="Calendar" />
      <div className="flex-1 overflow-y-auto p-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CalendarIcon className="h-5 w-5" />
              {new Date().toLocaleDateString("en-US", { month: "long", year: "numeric" })}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-7 gap-1">
              {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
                <div key={d} className="p-2 text-center text-xs font-medium text-slate-500">{d}</div>
              ))}
              {days.map((date, i) => (
                <div
                  key={i}
                  className={`min-h-[80px] rounded-lg border p-2 text-sm ${
                    date.toDateString() === today
                      ? "border-blue-600 bg-blue-50 dark:bg-blue-950"
                      : "border-slate-100 dark:border-slate-800"
                  }`}
                >
                  <span className={date.getMonth() !== new Date().getMonth() ? "text-slate-300" : ""}>
                    {date.getDate()}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
