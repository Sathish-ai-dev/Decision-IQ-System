import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Workflow, Zap, Clock, GitBranch } from "lucide-react";

export const Route = createFileRoute("/_authenticated/automation")({
  head: () => ({ meta: [{ title: "Automation — Decision IQ" }] }),
  component: AutomationPage,
});

const timeline = [
  { time: "09:00", event: "Daily data sync started", status: "active" },
  { time: "09:14", event: "AI insight scan completed", status: "active" },
  { time: "10:30", event: "Compliance report generated", status: "active" },
  { time: "11:45", event: "Vendor anomaly alert fired", status: "processing" },
  { time: "13:00", event: "Weekly digest email dispatched", status: "active" },
];

const cards = [
  { icon: Clock, name: "Scheduled sync", desc: "Hourly", runs: 720 },
  { icon: Zap, name: "Event triggered", desc: "On new document", runs: 148 },
  { icon: GitBranch, name: "Conditional flow", desc: "If KPI < threshold", runs: 22 },
];

const triggers = [
  { icon: Clock, name: "Schedule", desc: "Cron-based recurring runs" },
  { icon: Zap, name: "Event", desc: "New document, new dataset, etc." },
  { icon: Workflow, name: "AI signal", desc: "Anomaly, drift, insight generated" },
];

const rows = [
  { name: "Weekly compliance sync", trigger: "Schedule", last: "1 hr ago", status: "active" },
  { name: "New document processing", trigger: "Event", last: "2 min ago", status: "active" },
  { name: "Anomaly notification", trigger: "AI signal", last: "12 min ago", status: "processing" },
  { name: "Monthly board digest", trigger: "Schedule", last: "3 days ago", status: "draft" },
  { name: "Vendor onboarding flow", trigger: "Event", last: "last week", status: "archived" },
];

function AutomationPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Automation"
        description="Design event-driven, scheduled, and AI-triggered workflows."
        actions={<Button><Plus className="mr-1.5 h-4 w-4" /> New automation</Button>}
      />

      <div className="grid gap-4 lg:grid-cols-3">
        {cards.map((c) => (
          <Card key={c.name} className="shadow-elev-1">
            <CardContent className="p-5">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <c.icon className="h-4 w-4" />
              </div>
              <h3 className="mt-3 text-sm font-semibold">{c.name}</h3>
              <p className="text-xs text-muted-foreground">{c.desc}</p>
              <p className="mt-3 text-2xl font-semibold">{c.runs}</p>
              <p className="text-xs text-muted-foreground">runs this month</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="shadow-elev-1 lg:col-span-2">
          <CardContent className="p-5">
            <h3 className="text-sm font-semibold">Today's activity</h3>
            <ol className="relative mt-4 ml-3 border-l">
              {timeline.map((t, i) => (
                <li key={i} className="mb-4 ml-4">
                  <div className="absolute -left-1.5 h-3 w-3 rounded-full border bg-background ring-2 ring-primary/30" />
                  <div className="flex items-center gap-2">
                    <p className="text-xs text-muted-foreground">{t.time}</p>
                    <StatusBadge status={t.status} className="text-[10px]" />
                  </div>
                  <p className="text-sm">{t.event}</p>
                </li>
              ))}
            </ol>
          </CardContent>
        </Card>

        <Card className="shadow-elev-1">
          <CardContent className="p-5">
            <h3 className="text-sm font-semibold">Trigger types</h3>
            <div className="mt-4 space-y-3">
              {triggers.map((t) => (
                <div key={t.name} className="flex items-start gap-3 rounded-lg border p-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/10 text-primary">
                    <t.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium">{t.name}</p>
                    <p className="text-xs text-muted-foreground">{t.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="shadow-elev-1">
        <CardContent className="p-5">
          <h3 className="text-sm font-semibold">All automations</h3>
          <div className="mt-4 overflow-hidden rounded-lg border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Trigger</TableHead>
                  <TableHead>Last run</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((r) => (
                  <TableRow key={r.name}>
                    <TableCell className="font-medium">{r.name}</TableCell>
                    <TableCell className="text-muted-foreground">{r.trigger}</TableCell>
                    <TableCell className="text-muted-foreground">{r.last}</TableCell>
                    <TableCell><StatusBadge status={r.status} /></TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
