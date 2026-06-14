import { PublicHeader, PublicFooter } from "@/components/layout/public-header";
import { Brain, Target, Users, BarChart3, Mail, MessageSquare, Calendar, FileText } from "lucide-react";

const modules = [
  { icon: Users, title: "Lead Management", features: ["CSV Import/Export", "Bulk Actions", "Assignment Rules", "AI Lead Scoring"] },
  { icon: Target, title: "Opportunity Management", features: ["Pipeline Tracking", "Drag & Drop Kanban", "Win/Loss Analysis", "Revenue Tracking"] },
  { icon: Brain, title: "AI Module", features: ["Lead Scoring (XGBoost)", "Churn Prediction", "Revenue Forecasting", "Email Generation", "Sentiment Analysis"] },
  { icon: BarChart3, title: "Analytics & Reporting", features: ["Dashboard KPIs", "PDF/Excel Export", "Scheduled Reports", "Team Performance"] },
  { icon: Calendar, title: "Task & Calendar", features: ["Task Management", "Reminders", "Meeting Scheduling", "Team Assignment"] },
  { icon: Mail, title: "Communication", features: ["Contact History", "Timeline View", "Document Management", "Activity Tracking"] },
  { icon: MessageSquare, title: "Follow-Up AI", features: ["Best Action Recommendations", "Optimal Timing", "Channel Selection", "Template Generation"] },
  { icon: FileText, title: "Multi-Tenant SaaS", features: ["Organization Isolation", "RBAC", "Team Management", "Department Structure"] },
];

export const metadata = { title: "Features" };

export default function FeaturesPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <h1 className="text-4xl font-bold">Powerful Features for Modern Sales Teams</h1>
            <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
              Everything you need to manage leads, close deals, and grow revenue.
            </p>
          </div>
          <div className="mt-16 grid gap-8 md:grid-cols-2">
            {modules.map((mod) => (
              <div key={mod.title} className="rounded-xl border border-slate-200 p-8 dark:border-slate-800">
                <div className="mb-4 inline-flex rounded-lg bg-blue-50 p-3 text-blue-600 dark:bg-blue-950">
                  <mod.icon className="h-6 w-6" />
                </div>
                <h2 className="text-xl font-semibold">{mod.title}</h2>
                <ul className="mt-4 space-y-2">
                  {mod.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                      <span className="h-1.5 w-1.5 rounded-full bg-blue-600" /> {f}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
