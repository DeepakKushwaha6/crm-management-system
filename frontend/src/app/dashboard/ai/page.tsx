"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { DashboardHeader } from "@/components/layout/dashboard-sidebar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/store/auth";
import { aiApi } from "@/lib/api";
import { Brain, Mail, MessageSquare, TrendingUp, Users } from "lucide-react";

export default function AIPage() {
  const { tokens, organization } = useAuthStore();
  const [sentimentText, setSentimentText] = useState("");
  const [emailType, setEmailType] = useState("follow_up");
  const [emailContext, setEmailContext] = useState({ name: "John Doe", sender: "Sales Team", topic: "our partnership" });
  const [results, setResults] = useState<{
    sentiment?: { sentiment: string; confidence: number };
    email?: { subject: string; body: string };
    forecast?: { forecasts: Array<{ period: string; forecasted_revenue: number; confidence: number }> };
    followUp?: { recommended_action: string; best_channel: string; timing_days: number; urgency: string };
  }>({});

  const sentimentMutation = useMutation({
    mutationFn: () => aiApi.analyzeSentiment(tokens!.access, organization!.id, sentimentText),
    onSuccess: (data) => setResults((r) => ({ ...r, sentiment: data })),
  });

  const emailMutation = useMutation({
    mutationFn: () => aiApi.generateEmail(tokens!.access, organization!.id, emailType, emailContext),
    onSuccess: (data) => setResults((r) => ({ ...r, email: data })),
  });

  const forecastMutation = useMutation({
    mutationFn: () => aiApi.forecastRevenue(tokens!.access, organization!.id, "monthly"),
    onSuccess: (data) => setResults((r) => ({ ...r, forecast: data })),
  });

  const followUpMutation = useMutation({
    mutationFn: () => aiApi.followUp(tokens!.access, organization!.id, { status: "qualified", score: 85, entity_type: "lead" }),
    onSuccess: (data) => setResults((r) => ({ ...r, followUp: data })),
  });

  const tools = [
    { icon: MessageSquare, title: "Sentiment Analysis", action: () => sentimentMutation.mutate(), loading: sentimentMutation.isPending },
    { icon: Mail, title: "Email Generator", action: () => emailMutation.mutate(), loading: emailMutation.isPending },
    { icon: TrendingUp, title: "Revenue Forecast", action: () => forecastMutation.mutate(), loading: forecastMutation.isPending },
    { icon: Users, title: "Follow-Up Recommendation", action: () => followUpMutation.mutate(), loading: followUpMutation.isPending },
  ];

  return (
    <>
      <DashboardHeader title="AI Tools" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {tools.map((tool) => (
            <Card key={tool.title} className="cursor-pointer hover:shadow-md transition-shadow" onClick={tool.action}>
              <CardContent className="flex flex-col items-center p-6">
                <div className="mb-3 rounded-lg bg-blue-50 p-3 text-blue-600 dark:bg-blue-950">
                  <tool.icon className="h-6 w-6" />
                </div>
                <p className="text-sm font-medium text-center">{tool.title}</p>
                {tool.loading && <div className="mt-2 h-4 w-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />}
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><Brain className="h-5 w-5" /> Sentiment Analysis</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <Textarea placeholder="Enter text to analyze..." value={sentimentText} onChange={(e) => setSentimentText(e.target.value)} rows={4} />
              <Button onClick={() => sentimentMutation.mutate()} disabled={!sentimentText}>Analyze</Button>
              {results.sentiment && (
                <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-800">
                  <Badge variant={results.sentiment.sentiment === "positive" ? "success" : results.sentiment.sentiment === "negative" ? "destructive" : "secondary"}>
                    {results.sentiment.sentiment}
                  </Badge>
                  <p className="mt-2 text-sm">Confidence: {(results.sentiment.confidence * 100).toFixed(0)}%</p>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><Mail className="h-5 w-5" /> Email Generator</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <select className="w-full rounded-lg border border-slate-200 p-2 text-sm dark:border-slate-700 dark:bg-slate-900" value={emailType} onChange={(e) => setEmailType(e.target.value)}>
                <option value="follow_up">Follow Up</option>
                <option value="sales">Sales</option>
                <option value="meeting_request">Meeting Request</option>
                <option value="proposal">Proposal</option>
              </select>
              <Input placeholder="Recipient name" value={emailContext.name} onChange={(e) => setEmailContext({ ...emailContext, name: e.target.value })} />
              <Button onClick={() => emailMutation.mutate()}>Generate Email</Button>
              {results.email && (
                <div className="rounded-lg bg-slate-50 p-4 text-sm dark:bg-slate-800">
                  <p className="font-medium">{results.email.subject}</p>
                  <pre className="mt-2 whitespace-pre-wrap text-xs">{results.email.body}</pre>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {results.forecast && (
          <Card>
            <CardHeader><CardTitle>Revenue Forecast</CardTitle></CardHeader>
            <CardContent>
              <div className="grid gap-4 sm:grid-cols-3">
                {results.forecast.forecasts.map((f) => (
                  <div key={f.period} className="rounded-lg border p-4">
                    <p className="text-sm text-slate-500">{f.period}</p>
                    <p className="text-xl font-bold">${f.forecasted_revenue.toLocaleString()}</p>
                    <p className="text-xs text-slate-400">{(f.confidence * 100).toFixed(0)}% confidence</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {results.followUp && (
          <Card>
            <CardHeader><CardTitle>Follow-Up Recommendation</CardTitle></CardHeader>
            <CardContent>
              <p className="font-medium">{results.followUp.recommended_action}</p>
              <p className="mt-2 text-sm text-slate-500">Channel: {results.followUp.best_channel} · Timing: {results.followUp.timing_days} days · Urgency: {results.followUp.urgency}</p>
            </CardContent>
          </Card>
        )}
      </div>
    </>
  );
}
