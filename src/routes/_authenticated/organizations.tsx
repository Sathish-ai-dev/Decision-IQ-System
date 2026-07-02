import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Building2, Plus, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/_authenticated/organizations")({
  head: () => ({ meta: [{ title: "Organizations — Decision IQ" }] }),
  component: OrganizationsPage,
});

const orgs = [
  { name: "City of Aurora", members: 48, role: "Owner", plan: "Enterprise" },
  { name: "Northwind Analytics", members: 12, role: "Admin", plan: "Team" },
  { name: "Riverside Community", members: 6, role: "Member", plan: "Community" },
  { name: "Public Health Dept.", members: 24, role: "Analyst", plan: "Government" },
];

function OrganizationsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Organizations"
        description="Workspaces you belong to and their members."
        actions={<Button><Plus className="mr-1.5 h-4 w-4" /> New organization</Button>}
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {orgs.map((o) => (
          <Card key={o.name} className="shadow-elev-1">
            <CardContent className="p-5">
              <div className="flex items-start justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Building2 className="h-4 w-4" />
                </div>
                <Badge variant="outline">{o.plan}</Badge>
              </div>
              <h3 className="mt-3 text-sm font-semibold">{o.name}</h3>
              <p className="text-xs text-muted-foreground">{o.role}</p>
              <div className="mt-4 flex items-center justify-between border-t pt-3">
                <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <Users className="h-3 w-3" /> {o.members} members
                </span>
                <Button variant="ghost" size="sm">Manage</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
