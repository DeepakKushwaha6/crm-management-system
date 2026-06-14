"use client";

import { useState } from "react";
import { PublicHeader, PublicFooter } from "@/components/layout/public-header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/input";

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="flex min-h-screen flex-col">
      <PublicHeader />
      <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-xl">
          <h1 className="text-4xl font-bold">Contact Us</h1>
          <p className="mt-4 text-slate-600 dark:text-slate-400">
            Have questions? We would love to hear from you.
          </p>
          {submitted ? (
            <div className="mt-8 rounded-lg border border-green-200 bg-green-50 p-6 text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-200">
              Thank you for your message! We will get back to you within 24 hours.
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-8 space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium">Name</label>
                <Input required placeholder="Your name" />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Email</label>
                <Input required type="email" placeholder="you@company.com" />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Subject</label>
                <Input required placeholder="How can we help?" />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Message</label>
                <Textarea required rows={5} placeholder="Your message..." />
              </div>
              <Button type="submit" className="w-full">Send Message</Button>
            </form>
          )}
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
