import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lightbulb, TrendingUp, AlertTriangle, Target } from "lucide-react";

export const Route = createFileRoute("/_authenticated/insights")({
  head: () => ({ meta: [{ title: "Insights — Decision IQ" }] }),
  component: InsightsPage,
});

const insights = [
  { icon: TrendingUp, title: "Weekly query volume up 22%", body: "Citizen questions increased sharply. Consider adjusting staffing.", tag: "Trend", conf: 0.92 },
  { icon: AlertTriangle, title: "Anomaly in vendor invoices", body: "3 invoices exceeded budget by >15% this month.", tag: "Anomaly", conf: 0.87 },
  { icon: Target, title: "3 KPIs off-target", body: "Response time, resolution rate, and citizen NPS trending down.", tag: "KPI", conf: 0.78 },
  { icon: Lightbulb, title: "Consolidate duplicate datasets", body: "Datasets sales-2024 and revenue-2024 share 89% of rows.", tag: "Recommendation", conf: 0.81 },
  { icon: TrendingUp, title: "Automation opportunity", body: "You export the same report every Monday. Consider automating.", tag: "Opportunity", conf: 0.84 },
  { icon: AlertTriangle, title: "Data source stale", body: "Warehouse-West hasn't synced in 4 days.", tag: "Health", conf: 0.99 },
];

function InsightsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Insights"
        description="AI-generated observations, anomalies, and recommendations across your workspace."
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {insights.map((i) => (
          <Card key={i.title} className="shadow-elev-1">
            <CardContent className="p-5">
              <div className="flex items-start justify-between gap-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <i.icon className="h-4 w-4" />
                </div>
                <Badge variant="outline" className="text-[10px]">{i.tag}</Badge>
              </div>
              <h3 className="mt-3 text-sm font-semibold">{i.title}</h3>
              <p className="mt-1 text-sm text-muted-foreground">{i.body}</p>
              <div className="mt-4 flex items-center gap-2">
                <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
                  <div className="h-full bg-primary" style={{ width: `${i.conf * 100}%` }} />
                </div>
                <span className="text-xs text-muted-foreground">{Math.round(i.conf * 100)}%</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      <p className="text-xs text-muted-foreground">
        Insights are placeholders. AI-generated insights will replace this content in a later phase.
      </p>
    </div>
  );
}
