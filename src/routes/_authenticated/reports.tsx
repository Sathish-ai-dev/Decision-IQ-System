import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, Plus, FileBarChart, Calendar } from "lucide-react";

export const Route = createFileRoute("/_authenticated/reports")({
  head: () => ({ meta: [{ title: "Reports — Decision IQ" }] }),
  component: ReportsPage,
});

const reports = [
  { title: "Q3 Executive Summary", author: "Alice Chen", updated: "2 hr ago", status: "active" },
  { title: "Vendor Compliance Review", author: "Marcus Reed", updated: "yesterday", status: "draft" },
  { title: "Citizen Engagement KPIs", author: "Priya Patel", updated: "3 days ago", status: "active" },
  { title: "Budget Variance Analysis", author: "Dan Ross", updated: "last week", status: "archived" },
  { title: "Operations Weekly", author: "Sara Kim", updated: "2 hr ago", status: "active" },
  { title: "Public Sentiment Digest", author: "Ben Ortiz", updated: "yesterday", status: "processing" },
];

function ReportsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Curated summaries and exports across your workspace."
        actions={
          <>
            <Button variant="outline"><Download className="mr-1.5 h-4 w-4" /> Export</Button>
            <Button><Plus className="mr-1.5 h-4 w-4" /> New report</Button>
          </>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {reports.map((r) => (
          <Card key={r.title} className="shadow-elev-1 transition-shadow hover:shadow-elev-2">
            <CardContent className="p-5">
              <div className="flex items-start justify-between gap-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <FileBarChart className="h-4 w-4" />
                </div>
                <StatusBadge status={r.status} />
              </div>
              <h3 className="mt-3 text-sm font-semibold">{r.title}</h3>
              <p className="mt-1 text-xs text-muted-foreground">by {r.author}</p>
              <div className="mt-4 flex h-24 items-center justify-center rounded-md border border-dashed bg-muted/30">
                <p className="text-xs text-muted-foreground">Report preview placeholder</p>
              </div>
              <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
                <span className="flex items-center gap-1"><Calendar className="h-3 w-3" /> {r.updated}</span>
                <Button size="sm" variant="ghost" className="h-7">
                  <Download className="mr-1 h-3 w-3" /> Export
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
