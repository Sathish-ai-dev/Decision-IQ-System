import { createFileRoute, Link } from "@tanstack/react-router";
import { MarketingShell } from "@/components/layouts/MarketingShell";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Sparkles, Brain, Database, BarChart3, Workflow, ShieldCheck, Lightbulb, ArrowRight, CheckCircle2, Zap, Users,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Decision Intelligence Platform — AI-powered decision making" },
      { name: "description", content: "Turn data into decisions with an enterprise AI platform built for citizens, organizations, and government." },
    ],
  }),
  component: HomePage,
});

const features = [
  { icon: Brain, title: "AI Assistant", desc: "Ask questions of your data in natural language and get grounded answers." },
  { icon: Database, title: "Unified Data Sources", desc: "Connect databases, files, APIs, and warehouses in one governed layer." },
  { icon: Lightbulb, title: "AI Insights", desc: "Automatically surface trends, anomalies, and recommendations across your data." },
  { icon: BarChart3, title: "Enterprise Analytics", desc: "Interactive dashboards, KPIs, forecasts, and geographic intelligence." },
  { icon: Workflow, title: "Automation", desc: "Trigger workflows on events, schedules, and AI-detected signals." },
  { icon: ShieldCheck, title: "Governed & Secure", desc: "Role-based access, audit logs, and enterprise-grade compliance controls." },
];

const benefits = [
  "Reduce decision cycle time by up to 60%",
  "Ground every answer in your own data",
  "Empower every role — from citizen to analyst",
  "Governed, auditable, enterprise-ready",
];

const steps = [
  { n: "01", t: "Connect", d: "Bring your data sources, documents, and datasets into one place." },
  { n: "02", t: "Ask", d: "Chat with an AI assistant that understands your organization's context." },
  { n: "03", t: "Decide", d: "Act on insights, automate workflows, and share decisions with confidence." },
];

const stack = ["FastAPI", "Google Cloud", "Vertex AI", "Gemini", "LangChain", "ChromaDB", "PostgreSQL", "React"];

function HomePage() {
  return (
    <MarketingShell>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-primary/5 via-background to-background" />
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-28">
          <div className="mx-auto max-w-3xl text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full border bg-background px-3 py-1 text-xs font-medium text-muted-foreground shadow-elev-1">
              <Sparkles className="h-3 w-3 text-primary" /> Enterprise AI Decision Intelligence
            </span>
            <h1 className="mt-6 text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
              Turn data into <span className="text-primary">confident decisions</span>.
            </h1>
            <p className="mt-6 text-lg text-muted-foreground">
              A modern platform that unifies your data, documents, and AI — so every citizen, analyst,
              organization, and government team can decide with clarity.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <Button asChild size="lg">
                <Link to="/auth">Get started <ArrowRight className="ml-1.5 h-4 w-4" /></Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link to="/features">Explore features</Link>
              </Button>
            </div>
          </div>

          <div className="mx-auto mt-16 max-w-5xl">
            <div className="rounded-2xl border bg-card p-2 shadow-elev-3">
              <div className="rounded-xl bg-gradient-to-br from-primary/10 via-background to-background p-8">
                <div className="grid gap-4 sm:grid-cols-3">
                  {[
                    { k: "1,284", l: "Insights generated" },
                    { k: "42", l: "Data sources" },
                    { k: "98.7%", l: "Uptime SLA" },
                  ].map((s) => (
                    <div key={s.l} className="rounded-lg bg-card p-4 shadow-elev-1">
                      <p className="text-2xl font-semibold tracking-tight">{s.k}</p>
                      <p className="text-xs text-muted-foreground">{s.l}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">A platform for every decision</h2>
          <p className="mt-3 text-muted-foreground">
            Enterprise capabilities designed to scale from a single team to an entire government.
          </p>
        </div>
        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <Card key={f.title} className="border shadow-elev-1 transition-shadow hover:shadow-elev-2">
              <CardContent className="p-6">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <f.icon className="h-5 w-5" />
                </div>
                <h3 className="mt-4 text-base font-semibold">{f.title}</h3>
                <p className="mt-1.5 text-sm text-muted-foreground">{f.desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Benefits */}
      <section className="border-y bg-muted/30">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:px-8">
          <div>
            <h2 className="text-3xl font-semibold tracking-tight">Built for confident, auditable decisions</h2>
            <p className="mt-3 text-muted-foreground">
              Every answer is grounded in your data. Every action is auditable. Every user sees
              exactly what their role permits.
            </p>
          </div>
          <ul className="grid gap-3 sm:grid-cols-2">
            {benefits.map((b) => (
              <li key={b} className="flex items-start gap-2 rounded-xl bg-card p-4 shadow-elev-1">
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                <span className="text-sm">{b}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* How it works */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-semibold tracking-tight">How it works</h2>
          <p className="mt-3 text-muted-foreground">Three steps from raw data to decisions you can defend.</p>
        </div>
        <div className="mt-12 grid gap-5 md:grid-cols-3">
          {steps.map((s) => (
            <Card key={s.n} className="shadow-elev-1">
              <CardContent className="p-6">
                <span className="text-xs font-semibold text-primary">{s.n}</span>
                <h3 className="mt-3 text-lg font-semibold">{s.t}</h3>
                <p className="mt-1.5 text-sm text-muted-foreground">{s.d}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Technology */}
      <section className="border-y bg-muted/30">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-semibold tracking-tight">Built on trusted technology</h2>
            <p className="mt-3 text-muted-foreground">
              Modern, open, and enterprise-grade. Ready to scale on Google Cloud.
            </p>
          </div>
          <div className="mt-10 flex flex-wrap justify-center gap-2">
            {stack.map((s) => (
              <span key={s} className="rounded-full border bg-card px-4 py-1.5 text-sm shadow-elev-1">
                {s}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-semibold tracking-tight">Trusted by teams that decide at scale</h2>
        </div>
        <div className="mt-10 grid gap-5 md:grid-cols-3">
          {[
            { name: "City of Aurora", role: "Government agency", quote: "Decision IQ let our analysts answer citizen questions in minutes, not weeks." },
            { name: "Northwind Analytics", role: "Consulting firm", quote: "The insights layer surfaced trends we'd have missed in dashboards." },
            { name: "Riverside Community", role: "Community org", quote: "Finally a platform that treats our data like a first-class citizen." },
          ].map((t) => (
            <Card key={t.name} className="shadow-elev-1">
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <Users className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{t.name}</p>
                    <p className="text-xs text-muted-foreground">{t.role}</p>
                  </div>
                </div>
                <p className="mt-4 text-sm text-muted-foreground">"{t.quote}"</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-7xl px-4 pb-24 sm:px-6 lg:px-8">
        <div className="overflow-hidden rounded-3xl border bg-gradient-to-br from-primary to-primary/80 p-10 text-primary-foreground shadow-elev-3 sm:p-14">
          <div className="grid gap-6 lg:grid-cols-2 lg:items-center">
            <div>
              <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">Ready to decide with confidence?</h2>
              <p className="mt-3 max-w-xl text-primary-foreground/85">
                Start with a free workspace. Bring your data, invite your team, and unlock enterprise decision intelligence.
              </p>
            </div>
            <div className="flex flex-wrap gap-3 lg:justify-end">
              <Button asChild size="lg" variant="secondary">
                <Link to="/auth"><Zap className="mr-1.5 h-4 w-4" /> Create account</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-primary-foreground/40 bg-transparent text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground">
                <Link to="/contact">Talk to sales</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </MarketingShell>
  );
}
