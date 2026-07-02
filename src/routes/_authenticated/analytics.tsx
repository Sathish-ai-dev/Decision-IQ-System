import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { MetricCard, ChartCard } from "@/components/common/MetricCard";
import {
  Line, LineChart, Bar, BarChart, Pie, PieChart, Cell, Area, AreaChart,
  CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { TrendingUp, TrendingDown, Users, DollarSign, Activity, MapPin } from "lucide-react";

export const Route = createFileRoute("/_authenticated/analytics")({
  head: () => ({ meta: [{ title: "Analytics — Decision IQ" }] }),
  component: AnalyticsPage,
});

const line = [
  { m: "Jan", v: 42 }, { m: "Feb", v: 55 }, { m: "Mar", v: 61 }, { m: "Apr", v: 72 },
  { m: "May", v: 68 }, { m: "Jun", v: 84 }, { m: "Jul", v: 92 },
];
const bar = [
  { name: "Ops", a: 42, b: 28 }, { name: "Sales", a: 68, b: 51 },
  { name: "HR", a: 24, b: 18 }, { name: "IT", a: 55, b: 40 }, { name: "Finance", a: 38, b: 32 },
];
const pie = [
  { name: "Documents", value: 42 }, { name: "Datasets", value: 28 },
  { name: "Insights", value: 18 }, { name: "Reports", value: 12 },
];
const pieColors = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)"];
const forecast = [
  { m: "Jul", actual: 92, forecast: null }, { m: "Aug", actual: null, forecast: 100 },
  { m: "Sep", actual: null, forecast: 108 }, { m: "Oct", actual: null, forecast: 115 },
];
const timeline = [
  { time: "09:12", event: "Data pipeline sync completed" },
  { time: "10:04", event: "3 new insights generated" },
  { time: "11:37", event: "Weekly automation dispatched" },
  { time: "13:22", event: "Anomaly detected in vendor spend" },
  { time: "15:41", event: "Report exported by analyst" },
];

function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Analytics" description="KPIs, trends, forecasts, and geographic intelligence." />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard label="Total Queries" value="12.4K" icon={Activity} delta="+8.4% WoW" trend="up" />
        <MetricCard label="Active Users" value="1,284" icon={Users} delta="+142" trend="up" />
        <MetricCard label="Revenue Impact" value="$4.2M" icon={DollarSign} delta="+12% MoM" trend="up" />
        <MetricCard label="Avg. Response" value="1.2s" icon={TrendingDown} delta="-140ms" trend="up" />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ChartCard title="Line Chart" description="Query volume over time">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={line}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="m" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8 }} />
                <Line type="monotone" dataKey="v" stroke="var(--chart-1)" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Bar Chart" description="Activity by department">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={bar}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="name" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="a" fill="var(--chart-1)" radius={[6, 6, 0, 0]} />
                <Bar dataKey="b" fill="var(--chart-2)" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Pie Chart" description="Content distribution">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pie} dataKey="value" nameKey="name" innerRadius={50} outerRadius={90} paddingAngle={2}>
                  {pie.map((_, i) => <Cell key={i} fill={pieColors[i]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Area Chart" description="Cumulative growth">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={line}>
                <defs>
                  <linearGradient id="ac" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--chart-2)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="var(--chart-2)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="m" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8 }} />
                <Area type="monotone" dataKey="v" stroke="var(--chart-2)" fill="url(#ac)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ChartCard title="Heatmap" description="Activity by day and hour (placeholder)">
          <div className="grid grid-cols-24 gap-0.5" style={{ gridTemplateColumns: "repeat(24, minmax(0, 1fr))" }}>
            {Array.from({ length: 7 * 24 }).map((_, i) => {
              const intensity = ((i * 37) % 100) / 100;
              return (
                <div
                  key={i}
                  className="aspect-square rounded-sm"
                  style={{ backgroundColor: `color-mix(in oklch, var(--chart-1) ${intensity * 90 + 10}%, transparent)` }}
                  title={`Cell ${i}`}
                />
              );
            })}
          </div>
          <div className="mt-3 flex items-center justify-between text-[10px] text-muted-foreground">
            <span>Less</span>
            <span>More</span>
          </div>
        </ChartCard>

        <ChartCard title="Geographic Map" description="Regional distribution (placeholder)">
          <div className="relative flex h-64 items-center justify-center overflow-hidden rounded-lg bg-gradient-to-br from-primary/5 to-primary/10">
            <MapPin className="h-10 w-10 text-primary/40" />
            <div className="absolute left-6 top-6 rounded-md bg-card px-2 py-1 text-xs shadow-elev-1">West · 32%</div>
            <div className="absolute right-8 top-10 rounded-md bg-card px-2 py-1 text-xs shadow-elev-1">East · 41%</div>
            <div className="absolute bottom-8 left-1/3 rounded-md bg-card px-2 py-1 text-xs shadow-elev-1">Central · 27%</div>
          </div>
        </ChartCard>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ChartCard title="Forecast" description="3-month projection (placeholder)">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={forecast}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="m" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line dataKey="actual" stroke="var(--chart-1)" strokeWidth={2} />
                <Line dataKey="forecast" stroke="var(--chart-3)" strokeWidth={2} strokeDasharray="6 4" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Timeline" description="Recent workspace events">
          <ol className="relative ml-3 border-l">
            {timeline.map((t, i) => (
              <li key={i} className="mb-4 ml-4">
                <div className="absolute -left-1.5 h-3 w-3 rounded-full border bg-background ring-2 ring-primary/30" />
                <p className="text-xs text-muted-foreground">{t.time}</p>
                <p className="text-sm">{t.event}</p>
              </li>
            ))}
          </ol>
        </ChartCard>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        {[
          { label: "MoM Growth", value: "+18%", trend: "up" as const, icon: TrendingUp },
          { label: "Cost per Query", value: "$0.012", trend: "down" as const, icon: TrendingDown },
          { label: "Adoption Rate", value: "76%", trend: "up" as const, icon: Users },
        ].map((k) => (
          <MetricCard key={k.label} label={k.label} value={k.value} icon={k.icon} trend={k.trend} />
        ))}
      </div>
    </div>
  );
}
