import { PublicHeader, PublicFooter } from "@/components/layout/public-header";

export const metadata = { title: "Terms of Service" };

export default function TermsPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="prose prose-slate mx-auto max-w-3xl dark:prose-invert">
          <h1>Terms of Service</h1>
          <p>Last updated: {new Date().toLocaleDateString()}</p>
          <h2>Acceptance of Terms</h2>
          <p>By accessing CRM AI PRO, you agree to these Terms of Service and our Privacy Policy.</p>
          <h2>Service Description</h2>
          <p>CRM AI PRO provides a cloud-based CRM platform with AI-powered features including lead scoring, churn prediction, and revenue forecasting.</p>
          <h2>User Responsibilities</h2>
          <p>You are responsible for maintaining the confidentiality of your account credentials and for all activities under your account.</p>
          <h2>Data Ownership</h2>
          <p>You retain ownership of all data you input into the platform. We process data solely to provide the service.</p>
          <h2>Limitation of Liability</h2>
          <p>CRM AI PRO is provided &quot;as is.&quot; We are not liable for indirect, incidental, or consequential damages arising from use of the service.</p>
          <h2>Contact</h2>
          <p>For legal inquiries, contact legal@crmaipro.com.</p>
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
