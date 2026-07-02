import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { PageHeader } from "@/components/common/EmptyState";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sparkles, Send, Plus, MessageSquare, ChevronRight } from "lucide-react";

export const Route = createFileRoute("/_authenticated/ai-assistant")({
  head: () => ({ meta: [{ title: "AI Assistant — Decision IQ" }] }),
  component: AIAssistantPage,
});

const suggested = [
  "Summarize this quarter's citizen feedback",
  "What datasets are missing metadata?",
  "Show me automations that failed last week",
  "Compare KPIs vs. last month",
];

const recent = [
  { title: "Budget analysis Q3", when: "2h ago" },
  { title: "Citizen sentiment overview", when: "Yesterday" },
  { title: "Vendor spend anomalies", when: "3 days ago" },
  { title: "Compliance readiness", when: "Last week" },
];

const demo = [
  { role: "assistant" as const, content: "Welcome to Decision IQ. Ask me anything about your data, documents, or KPIs." },
];

function AIAssistantPage() {
  const [input, setInput] = useState("");
  return (
    <div className="space-y-6">
      <PageHeader title="AI Assistant" description="Chat with your data — grounded in your organization's context." />
      <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
        <Card className="shadow-elev-1">
          <CardContent className="p-4">
            <Button className="w-full" size="sm"><Plus className="mr-1.5 h-4 w-4" /> New chat</Button>
            <div className="mt-4">
              <p className="px-1 text-xs font-medium text-muted-foreground">Recent chats</p>
              <ScrollArea className="mt-2 h-[420px]">
                <ul className="space-y-1">
                  {recent.map((r) => (
                    <li key={r.title}>
                      <button className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-sm hover:bg-accent">
                        <MessageSquare className="h-3.5 w-3.5 text-muted-foreground" />
                        <span className="flex-1 truncate">{r.title}</span>
                        <span className="text-[10px] text-muted-foreground">{r.when}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </ScrollArea>
            </div>
          </CardContent>
        </Card>

        <Card className="flex min-h-[560px] flex-col shadow-elev-1">
          <CardContent className="flex flex-1 flex-col p-0">
            <ScrollArea className="flex-1 p-6">
              <div className="space-y-4">
                {demo.map((m, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary">
                      <Sparkles className="h-4 w-4" />
                    </div>
                    <div className="rounded-xl bg-muted px-4 py-2.5 text-sm">{m.content}</div>
                  </div>
                ))}
              </div>
              <div className="mt-8">
                <p className="text-xs font-medium text-muted-foreground">Try asking</p>
                <div className="mt-2 grid gap-2 sm:grid-cols-2">
                  {suggested.map((s) => (
                    <button
                      key={s}
                      onClick={() => setInput(s)}
                      className="group flex items-center justify-between gap-2 rounded-lg border p-3 text-left text-sm hover:border-primary/40 hover:bg-accent"
                    >
                      <span>{s}</span>
                      <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-foreground" />
                    </button>
                  ))}
                </div>
              </div>
            </ScrollArea>
            <div className="border-t p-4">
              <form
                onSubmit={(e) => { e.preventDefault(); setInput(""); }}
                className="flex items-center gap-2"
              >
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask a question about your data..."
                  className="h-11"
                />
                <Button type="submit" size="lg" disabled={!input.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </form>
              <p className="mt-2 text-[11px] text-muted-foreground">
                AI logic is not yet implemented — this is a UI placeholder.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
