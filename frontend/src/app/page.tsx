import Link from "next/link";
import { PublicHeader, PublicFooter } from "@/components/layout/public-header";
import { Button } from "@/components/ui/button";
import {
  Brain, Target, BarChart3, Users, Zap, Shield, ArrowRight, CheckCircle,
} from "lucide-react";

const features = [
  { icon: Brain, title: "AI Lead Scoring", desc: "Predict conversion probability with ML models" },
  { icon: Target, title: "Pipeline Management", desc: "Drag-and-drop Kanban for deal tracking" },
  { icon: BarChart3, title: "Revenue Forecasting", desc: "AI-powered revenue predictions" },
  { icon: Users, title: "Multi-Tenant SaaS", desc: "Enterprise-grade tenant isolation" },
  { icon: Zap, title: "Automation", desc: "Smart follow-ups and email generation" },
  { icon: Shield, title: "Enterprise Security", desc: "RBAC, JWT, audit logging, OWASP compliant" },
];

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1">
        <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-indigo-50 px-4 py-24 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-7xl text-center">
            <div className="mb-6 inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-sm text-blue-700 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-300">
              <Brain className="mr-2 h-4 w-4" /> AI-Powered CRM Platform
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl dark:text-white">
              Close More Deals with{" "}
              <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                AI Intelligence
              </span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-300">
              CRM AI PRO combines enterprise CRM capabilities with machine learning to help your sales team
              prioritize leads, predict churn, and forecast revenue with precision.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Link href="/register">
                <Button size="lg" className="gap-2">
                  Start Free Trial <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/features">
                <Button variant="outline" size="lg">Explore Features</Button>
              </Link>
            </div>
            <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-sm text-slate-500">
              {["No credit card required", "14-day free trial", "Enterprise security"].map((t) => (
                <span key={t} className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" /> {t}
                </span>
              ))}
            </div>
          </div>
        </section>

        <section className="px-4 py-24 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="text-center">
              <h2 className="text-3xl font-bold">Everything You Need to Scale Sales</h2>
              <p className="mt-4 text-slate-600 dark:text-slate-400">
                Built for enterprise teams who demand performance, security, and intelligence.
              </p>
            </div>
            <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {features.map((f) => (
                <div
                  key={f.title}
                  className="rounded-xl border border-slate-200 p-6 transition-shadow hover:shadow-lg dark:border-slate-800"
                >
                  <div className="mb-4 inline-flex rounded-lg bg-blue-50 p-3 text-blue-600 dark:bg-blue-950 dark:text-blue-400">
                    <f.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-lg font-semibold">{f.title}</h3>
                  <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-blue-600 px-4 py-16 text-white sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl text-center">
            <h2 className="text-3xl font-bold">Ready to Transform Your Sales?</h2>
            <p className="mt-4 text-blue-100">Join thousands of sales teams using CRM AI PRO.</p>
            <Link href="/register" className="mt-8 inline-block">
              <Button size="lg" variant="secondary" className="gap-2">
                Get Started Free <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </section>
      </main>
      <PublicFooter />
    </div>
  );
}
