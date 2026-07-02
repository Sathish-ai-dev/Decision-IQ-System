import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Plus, Search } from "lucide-react";

export const Route = createFileRoute("/_authenticated/users")({
  head: () => ({ meta: [{ title: "Users — Decision IQ" }] }),
  component: UsersPage,
});

const users = [
  { name: "Alice Chen", email: "alice@aurora.gov", role: "Admin", org: "City of Aurora", status: "active" },
  { name: "Marcus Reed", email: "marcus@northwind.com", role: "Analyst", org: "Northwind Analytics", status: "active" },
  { name: "Priya Patel", email: "priya@publichealth.org", role: "Analyst", org: "Public Health Dept.", status: "active" },
  { name: "Dan Ross", email: "dan@aurora.gov", role: "Organization", org: "City of Aurora", status: "active" },
  { name: "Sara Kim", email: "sara@riverside.org", role: "Community", org: "Riverside Community", status: "active" },
  { name: "Ben Ortiz", email: "ben@citizen.example", role: "Citizen", org: "—", status: "active" },
];

function UsersPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Users"
        description="Members with access to your workspaces."
        actions={<Button><Plus className="mr-1.5 h-4 w-4" /> Invite user</Button>}
      />
      <Card className="shadow-elev-1">
        <CardContent className="p-5">
          <div className="relative w-full sm:max-w-xs">
            <Search className="pointer-events-none absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input placeholder="Search users..." className="pl-8" />
          </div>
          <div className="mt-4 overflow-hidden rounded-lg border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>User</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Organization</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((u) => (
                  <TableRow key={u.email}>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="bg-primary text-xs text-primary-foreground">
                            {u.name.split(" ").map(n => n[0]).join("")}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm font-medium">{u.name}</p>
                          <p className="text-xs text-muted-foreground">{u.email}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell><Badge variant="outline">{u.role}</Badge></TableCell>
                    <TableCell className="text-muted-foreground">{u.org}</TableCell>
                    <TableCell>
                      <span className="inline-flex items-center gap-1.5 text-xs text-success">
                        <span className="h-1.5 w-1.5 rounded-full bg-success" /> {u.status}
                      </span>
                    </TableCell>
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
