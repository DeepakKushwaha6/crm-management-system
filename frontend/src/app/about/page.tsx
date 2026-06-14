import { PublicHeader, PublicFooter } from "@/components/layout/public-header";

export const metadata = { title: "About" };

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="text-4xl font-bold">About CRM AI PRO</h1>
          <p className="mt-6 text-lg text-slate-600 dark:text-slate-400">
            CRM AI PRO is an enterprise-grade, AI-powered CRM SaaS platform built for modern sales teams.
            We combine the power of machine learning with intuitive CRM workflows to help organizations
            close more deals, retain customers, and forecast revenue with confidence.
          </p>
          <h2 className="mt-12 text-2xl font-semibold">Our Mission</h2>
          <p className="mt-4 text-slate-600 dark:text-slate-400">
            To democratize enterprise CRM capabilities by making AI-powered sales intelligence accessible
            to teams of all sizes. We believe every sales professional deserves the tools that Fortune 500
            companies use to drive growth.
          </p>
          <h2 className="mt-12 text-2xl font-semibold">Why Choose Us</h2>
          <ul className="mt-4 space-y-3 text-slate-600 dark:text-slate-400">
            <li>• Multi-tenant architecture supporting thousands of organizations</li>
            <li>• AI models trained on real sales patterns (XGBoost, Random Forest)</li>
            <li>• Enterprise security with RBAC, JWT, and audit logging</li>
            <li>• 99.9% uptime SLA for enterprise customers</li>
            <li>• Open API with Swagger documentation</li>
          </ul>
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
