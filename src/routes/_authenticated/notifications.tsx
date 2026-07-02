import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Bell, AlertTriangle, CheckCircle2, Sparkles, Workflow } from "lucide-react";

export const Route = createFileRoute("/_authenticated/notifications")({
  head: () => ({ meta: [{ title: "Notifications — Decision IQ" }] }),
  component: NotificationsPage,
});

const notifs = [
  { icon: Sparkles, title: "New insight available", body: "3 new insights generated overnight.", when: "2 min ago", unread: true },
  { icon: AlertTriangle, title: "Data source failed", body: "Warehouse-West hasn't synced in 4 days.", when: "1 hr ago", unread: true },
  { icon: Workflow, title: "Automation completed", body: "Weekly compliance sync finished successfully.", when: "3 hr ago", unread: false },
  { icon: CheckCircle2, title: "Report shared with your team", body: "Q3 Executive Summary was shared.", when: "yesterday", unread: false },
  { icon: Bell, title: "New team member joined", body: "Ben Ortiz joined Riverside Community.", when: "2 days ago", unread: false },
];

function NotificationsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Notifications"
        description="Alerts, updates, and activity from your workspaces."
        actions={<Button variant="outline">Mark all as read</Button>}
      />
      <Card className="shadow-elev-1">
        <CardContent className="p-0">
          <ul className="divide-y">
            {notifs.map((n, i) => (
              <li key={i} className="flex items-start gap-3 p-4">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                  <n.icon className="h-4 w-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-medium">{n.title}</p>
                    {n.unread && <span className="h-1.5 w-1.5 rounded-full bg-primary" />}
                  </div>
                  <p className="mt-0.5 text-sm text-muted-foreground">{n.body}</p>
                </div>
                <span className="shrink-0 text-xs text-muted-foreground">{n.when}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
