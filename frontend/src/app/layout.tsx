import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { QueryProvider } from "@/providers/query-provider";
import { ThemeProvider } from "@/providers/theme-provider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "CRM AI PRO - Enterprise AI-Powered CRM",
    template: "%s | CRM AI PRO",
  },
  description:
    "Enterprise-grade AI-powered CRM SaaS platform. Lead scoring, pipeline management, revenue forecasting, and more.",
  keywords: ["CRM", "AI", "Sales", "SaaS", "Lead Management", "Pipeline"],
  openGraph: {
    title: "CRM AI PRO",
    description: "Enterprise AI-Powered CRM SaaS Platform",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full`} suppressHydrationWarning>
      <body className="min-h-full font-sans antialiased">
        <QueryProvider>
          <ThemeProvider>{children}</ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
