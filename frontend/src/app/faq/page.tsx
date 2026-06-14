"use client";

import { useState } from "react";
import { PublicHeader, PublicFooter } from "@/components/layout/public-header";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

const faqs = [
  { q: "What is CRM AI PRO?", a: "CRM AI PRO is an enterprise-grade, AI-powered CRM SaaS platform that helps sales teams manage leads, track deals, and leverage machine learning for lead scoring, churn prediction, and revenue forecasting." },
  { q: "How does AI lead scoring work?", a: "Our AI models (XGBoost and Random Forest) analyze lead attributes including source, status, contact completeness, and engagement patterns to predict conversion probability on a 0-100 scale." },
  { q: "Is my data secure?", a: "Yes. We implement JWT authentication, RBAC, row-level tenant isolation, audit logging, rate limiting, and OWASP Top 10 compliance. All data is encrypted in transit and at rest." },
  { q: "Can I import existing leads?", a: "Absolutely. You can import leads via CSV with bulk actions for assignment and status updates. Export functionality is also available." },
  { q: "What roles are supported?", a: "We support Super Admin, Organization Admin, Sales Manager, Sales Executive, and Read-Only User roles with granular RBAC permissions." },
  { q: "Do you offer a free trial?", a: "Yes, all plans include a 14-day free trial with full access to Professional features. No credit card required." },
  { q: "Can I deploy on-premises?", a: "Enterprise customers can deploy using our Docker Compose setup with full source access. Contact sales for on-premises licensing." },
  { q: "What integrations are available?", a: "Our REST API with OpenAPI/Swagger documentation supports custom integrations. Enterprise plans include webhook support and dedicated integration assistance." },
];

export default function FAQPage() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="text-4xl font-bold">Frequently Asked Questions</h1>
          <p className="mt-4 text-slate-600 dark:text-slate-400">Find answers to common questions about CRM AI PRO.</p>
          <div className="mt-12 space-y-4">
            {faqs.map((faq, i) => (
              <div key={i} className="rounded-lg border border-slate-200 dark:border-slate-800">
                <button
                  className="flex w-full items-center justify-between p-4 text-left font-medium"
                  onClick={() => setOpen(open === i ? null : i)}
                >
                  {faq.q}
                  <ChevronDown className={cn("h-5 w-5 transition-transform", open === i && "rotate-180")} />
                </button>
                {open === i && (
                  <div className="border-t border-slate-200 px-4 py-3 text-sm text-slate-600 dark:border-slate-800 dark:text-slate-400">
                    {faq.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
