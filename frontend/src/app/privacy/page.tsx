import { PublicHeader, PublicFooter } from "@/components/layout/public-header";

export const metadata = { title: "Privacy Policy" };

export default function PrivacyPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="prose prose-slate mx-auto max-w-3xl dark:prose-invert">
          <h1>Privacy Policy</h1>
          <p>Last updated: {new Date().toLocaleDateString()}</p>
          <h2>Information We Collect</h2>
          <p>We collect information you provide directly, including account registration data, CRM records you create, and usage analytics to improve our service.</p>
          <h2>How We Use Information</h2>
          <p>Your data is used to provide CRM services, AI predictions, and platform improvements. We never sell your data to third parties.</p>
          <h2>Data Security</h2>
          <p>We implement industry-standard security measures including encryption, access controls, and regular security audits.</p>
          <h2>Data Retention</h2>
          <p>Data is retained while your account is active. Upon account deletion, data is permanently removed within 30 days.</p>
          <h2>Contact</h2>
          <p>For privacy inquiries, contact us at privacy@crmaipro.com.</p>
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
