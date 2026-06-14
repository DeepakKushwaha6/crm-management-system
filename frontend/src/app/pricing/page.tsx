import Link from "next/link";
import { PublicHeader, PublicFooter } from "@/components/layout/public-header";
import { Button } from "@/components/ui/button";
import { CheckCircle } from "lucide-react";

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    desc: "For small teams getting started",
    features: ["Up to 3 users", "500 leads", "Basic CRM", "Email support"],
    cta: "Get Started",
    popular: false,
  },
  {
    name: "Professional",
    price: "$49",
    period: "/user/month",
    desc: "For growing sales teams",
    features: ["Unlimited users", "Unlimited leads", "AI Lead Scoring", "Pipeline Analytics", "CSV Import/Export", "Priority support"],
    cta: "Start Free Trial",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "contact us",
    desc: "For large organizations",
    features: ["Everything in Pro", "AI Churn Prediction", "Revenue Forecasting", "Custom integrations", "Dedicated support", "SLA guarantee", "SSO & Advanced RBAC"],
    cta: "Contact Sales",
    popular: false,
  },
];

export const metadata = { title: "Pricing" };

export default function PricingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <h1 className="text-4xl font-bold">Simple, Transparent Pricing</h1>
            <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
              Choose the plan that fits your team. All plans include a 14-day free trial.
            </p>
          </div>
          <div className="mt-16 grid gap-8 lg:grid-cols-3">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-xl border p-8 ${
                  plan.popular
                    ? "border-blue-600 shadow-lg shadow-blue-600/10"
                    : "border-slate-200 dark:border-slate-800"
                }`}
              >
                {plan.popular && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold text-white">
                    Most Popular
                  </span>
                )}
                <h2 className="text-xl font-semibold">{plan.name}</h2>
                <p className="mt-1 text-sm text-slate-500">{plan.desc}</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="text-sm text-slate-500"> {plan.period}</span>
                </div>
                <ul className="mt-6 space-y-3">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm">
                      <CheckCircle className="h-4 w-4 text-green-500" /> {f}
                    </li>
                  ))}
                </ul>
                <Link href={plan.name === "Enterprise" ? "/contact" : "/register"} className="mt-8 block">
                  <Button className="w-full" variant={plan.popular ? "default" : "outline"}>
                    {plan.cta}
                  </Button>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
