import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { MetricCard, ChartCard } from "@/components/common/MetricCard";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Database, FileText, Lightbulb, Workflow, Building2, Sparkles, ArrowRight, Activity, TrendingUp, Upload, FolderKanban, FileBarChart } from "lucide-react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export const Route = createFileRoute("/_authenticated/dashboard")({
  head: () => ({ meta: [{ title: "Dashboard — Decision IQ" }] }),
  component: DashboardPage,
});

const chartData = [
  { m: "Jan", queries: 240, insights: 32 },
  { m: "Feb", queries: 310, insights: 41 },
  { m: "Mar", queries: 420, insights: 58 },
  { m: "Apr", queries: 380, insights: 62 },
  { m: "May", queries: 520, insights: 74 },
  { m: "Jun", queries: 610, insights: 88 },
  { m: "Jul", queries: 740, insights: 103 },
];

const activity = [
  { icon: Upload, title: "New document uploaded", meta: "Annual budget FY25.pdf • 2 min ago" },
  { icon: Sparkles, title: "AI insight generated", meta: "Anomaly detected in weekly usage • 12 min ago" },
  { icon: Workflow, title: "Automation ran", meta: "Weekly compliance sync • 1 hr ago" },
  { icon: Database, title: "Data source connected", meta: "Warehouse-East (PostgreSQL) • 3 hr ago" },
];

const recommendations = [
  { title: "Investigate spike in citizen queries", body: "Query volume grew 22% WoW. Consider staffing review.", tag: "Trend" },
  { title: "Consolidate duplicate datasets", body: "3 datasets share >85% overlap. Merging could reduce cost.", tag: "Efficiency" },
  { title: "Enable automation for weekly reports", body: "You export the same report every Monday.", tag: "Automation" },
];

function DashboardPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Welcome back"
        description="Here's what's happening across your Decision Intelligence workspace."
        actions={
          <>
            <Button asChild variant="outline"><Link to="/ai-assistant"><Sparkles className="mr-1.5 h-4 w-4" /> Ask AI</Link></Button>
            <Button asChild><Link to="/data-sources"><Database className="mr-1.5 h-4 w-4" /> Connect data</Link></Button>
          </>
        }
      />

      {/* Metric cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard label="Connected Data Sources" value="12" icon={Database} delta="+2 this month" trend="up" />
        <MetricCard label="Uploaded Documents" value="248" icon={FileText} delta="+34 this week" trend="up" />
        <MetricCard label="Generated Insights" value="86" icon={Lightbulb} delta="+12 today" trend="up" />
        <MetricCard label="Active Automations" value="7" icon={Workflow} delta="1 needs attention" trend="neutral" />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <MetricCard label="Organizations" value="4" icon={Building2} hint="1 pending invitation" className="lg:col-span-1" />
        <MetricCard label="Team members" value="28" icon={Sparkles} hint="6 analysts, 22 viewers" className="lg:col-span-1" />
        <MetricCard label="Reports this month" value="19" icon={FileBarChart} delta="+4 vs last month" trend="up" className="lg:col-span-1" />
      </div>

      {/* Analytics overview + AI Recommendations */}
      <div className="grid gap-4 lg:grid-cols-3">
        <ChartCard
          title="Analytics Overview"
          description="Queries and AI-generated insights over the last 7 months"
          className="lg:col-span-2"
          action={<Button asChild variant="ghost" size="sm"><Link to="/analytics">View <ArrowRight className="ml-1 h-3.5 w-3.5" /></Link></Button>}
        >
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="c1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--chart-1)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="var(--chart-1)" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="c2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--chart-2)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="var(--chart-2)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="m" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8 }} />
                <Area type="monotone" dataKey="queries" stroke="var(--chart-1)" fill="url(#c1)" strokeWidth={2} />
                <Area type="monotone" dataKey="insights" stroke="var(--chart-2)" fill="url(#c2)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <Card className="shadow-elev-1">
          <CardContent className="p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold">AI Recommendations</h3>
                <p className="text-xs text-muted-foreground">Placeholder — grounded suggestions will appear here</p>
              </div>
              <Sparkles className="h-4 w-4 text-primary" />
            </div>
            <div className="space-y-3">
              {recommendations.map((r) => (
                <div key={r.title} className="rounded-lg border p-3">
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-sm font-medium">{r.title}</p>
                    <Badge variant="outline" className="shrink-0 text-[10px]">{r.tag}</Badge>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">{r.body}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent activity + quick actions */}
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="shadow-elev-1 lg:col-span-2">
          <CardContent className="p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold">Recent Activity</h3>
                <p className="text-xs text-muted-foreground">Latest events across your workspace</p>
              </div>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </div>
            <ul className="divide-y">
              {activity.map((a, i) => (
                <li key={i} className="flex items-center gap-3 py-3">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                    <a.icon className="h-4 w-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium">{a.title}</p>
                    <p className="truncate text-xs text-muted-foreground">{a.meta}</p>
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card className="shadow-elev-1">
          <CardContent className="p-5">
            <h3 className="text-sm font-semibold">Quick actions</h3>
            <div className="mt-4 grid grid-cols-2 gap-2">
              {[
                { icon: Sparkles, label: "Ask AI", to: "/ai-assistant" },
                { icon: Upload, label: "Upload doc", to: "/documents" },
                { icon: Database, label: "New source", to: "/data-sources" },
                { icon: FolderKanban, label: "New dataset", to: "/datasets" },
                { icon: FileBarChart, label: "New report", to: "/reports" },
                { icon: Workflow, label: "Automation", to: "/automation" },
              ].map((q) => (
                <Button key={q.label} asChild variant="outline" className="h-auto justify-start gap-2 py-3">
                  <Link to={q.to}>
                    <q.icon className="h-4 w-4 text-primary" />
                    <span className="text-sm">{q.label}</span>
                  </Link>
                </Button>
              ))}
            </div>
            <div className="mt-4 rounded-lg border bg-muted/30 p-3">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-success" />
                <p className="text-xs font-medium">Weekly summary</p>
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                Your team asked 22% more questions this week. AI insights up 18%.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
