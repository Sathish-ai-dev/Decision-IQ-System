import { createFileRoute } from "@tanstack/react-router";
import { MarketingShell } from "@/components/layouts/MarketingShell";
import { Card, CardContent } from "@/components/ui/card";
import { Brain, Database, BarChart3, Workflow, ShieldCheck, Lightbulb, FileText, Sparkles, Users } from "lucide-react";

export const Route = createFileRoute("/features")({
  head: () => ({
    meta: [
      { title: "Features — Decision Intelligence Platform" },
      { name: "description", content: "Explore AI Assistant, insights, data sources, analytics, automation, and enterprise-grade security." },
    ],
  }),
  component: FeaturesPage,
});

const groups = [
  {
    title: "AI",
    items: [
      { icon: Brain, name: "AI Assistant", desc: "Natural-language chat grounded in your data." },
      { icon: Lightbulb, name: "Insights", desc: "Automatic detection of trends, anomalies, and recommendations." },
      { icon: Sparkles, name: "Suggestions", desc: "Suggested questions and next best actions." },
    ],
  },
  {
    title: "Data",
    items: [
      { icon: Database, name: "Data Sources", desc: "Connect databases, warehouses, and APIs." },
      { icon: FileText, name: "Documents", desc: "Upload and organize documents with metadata." },
      { icon: Users, name: "Organizations", desc: "Team, project, and role-scoped data spaces." },
    ],
  },
  {
    title: "Analytics & Automation",
    items: [
      { icon: BarChart3, name: "Analytics", desc: "Interactive charts, KPIs, forecasting, and heatmaps." },
      { icon: Workflow, name: "Automation", desc: "Event, schedule, and AI-triggered workflows." },
      { icon: ShieldCheck, name: "Governance", desc: "RBAC, audit logs, and enterprise controls." },
    ],
  },
];

function FeaturesPage() {
  return (
    <MarketingShell>
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-semibold tracking-tight">Everything you need to decide</h1>
          <p className="mt-3 text-muted-foreground">
            A cohesive platform for AI, data, analytics, and automation — designed for enterprise scale.
          </p>
        </div>
        <div className="mt-14 space-y-14">
          {groups.map((g) => (
            <div key={g.title}>
              <h2 className="text-xl font-semibold">{g.title}</h2>
              <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {g.items.map((f) => (
                  <Card key={f.name} className="shadow-elev-1">
                    <CardContent className="p-5">
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                        <f.icon className="h-4 w-4" />
                      </div>
                      <h3 className="mt-3 text-sm font-semibold">{f.name}</h3>
                      <p className="mt-1 text-sm text-muted-foreground">{f.desc}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </MarketingShell>
  );
}
