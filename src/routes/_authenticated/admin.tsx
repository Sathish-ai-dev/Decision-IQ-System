import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ShieldCheck } from "lucide-react";

export const Route = createFileRoute("/_authenticated/admin")({
  head: () => ({ meta: [{ title: "Admin — Decision IQ" }] }),
  component: AdminPage,
});

const users = [
  { name: "Alice Chen", email: "alice@aurora.gov", roles: ["Admin"] },
  { name: "Marcus Reed", email: "marcus@northwind.com", roles: ["Analyst"] },
  { name: "Priya Patel", email: "priya@publichealth.org", roles: ["Analyst"] },
  { name: "Ben Ortiz", email: "ben@citizen.example", roles: ["Citizen"] },
];

const roles = [
  { role: "Admin", perms: 42, members: 3 },
  { role: "Analyst", perms: 28, members: 12 },
  { role: "Organization", perms: 22, members: 6 },
  { role: "Community", perms: 12, members: 34 },
  { role: "Citizen", perms: 6, members: 187 },
];

const orgs = [
  { name: "City of Aurora", members: 48, plan: "Enterprise" },
  { name: "Northwind Analytics", members: 12, plan: "Team" },
  { name: "Riverside Community", members: 6, plan: "Community" },
];

const audit = [
  { at: "10:24", actor: "alice@aurora.gov", action: "Granted role", target: "marcus (Analyst)" },
  { at: "09:12", actor: "system", action: "Automation ran", target: "compliance-weekly" },
  { at: "yesterday", actor: "priya@publichealth.org", action: "Uploaded document", target: "policy-v3.docx" },
  { at: "yesterday", actor: "dan@aurora.gov", action: "Connected data source", target: "warehouse-east" },
];

function AdminPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Admin"
        description="Manage users, roles, organizations, and workspace-wide activity."
        actions={<Badge variant="outline" className="gap-1"><ShieldCheck className="h-3 w-3" /> Admin access</Badge>}
      />
      <Tabs defaultValue="users">
        <TabsList>
          <TabsTrigger value="users">Users</TabsTrigger>
          <TabsTrigger value="roles">Roles</TabsTrigger>
          <TabsTrigger value="orgs">Organizations</TabsTrigger>
          <TabsTrigger value="audit">Audit log</TabsTrigger>
        </TabsList>

        <TabsContent value="users" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="p-5">
            <div className="overflow-hidden rounded-lg border">
              <Table>
                <TableHeader><TableRow>
                  <TableHead>Name</TableHead><TableHead>Email</TableHead><TableHead>Roles</TableHead><TableHead></TableHead>
                </TableRow></TableHeader>
                <TableBody>
                  {users.map((u) => (
                    <TableRow key={u.email}>
                      <TableCell className="font-medium">{u.name}</TableCell>
                      <TableCell className="text-muted-foreground">{u.email}</TableCell>
                      <TableCell><div className="flex gap-1">{u.roles.map(r => <Badge key={r} variant="outline">{r}</Badge>)}</div></TableCell>
                      <TableCell className="text-right"><Button size="sm" variant="ghost">Manage</Button></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="roles" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="p-5">
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {roles.map((r) => (
                <Card key={r.role} className="shadow-none border">
                  <CardContent className="p-4">
                    <p className="text-sm font-semibold">{r.role}</p>
                    <p className="mt-1 text-xs text-muted-foreground">{r.perms} permissions · {r.members} members</p>
                    <Button size="sm" variant="outline" className="mt-3">Edit</Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="orgs" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="p-5">
            <div className="overflow-hidden rounded-lg border">
              <Table>
                <TableHeader><TableRow>
                  <TableHead>Name</TableHead><TableHead>Members</TableHead><TableHead>Plan</TableHead>
                </TableRow></TableHeader>
                <TableBody>
                  {orgs.map((o) => (
                    <TableRow key={o.name}>
                      <TableCell className="font-medium">{o.name}</TableCell>
                      <TableCell>{o.members}</TableCell>
                      <TableCell><Badge variant="outline">{o.plan}</Badge></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="audit" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="p-5">
            <div className="overflow-hidden rounded-lg border">
              <Table>
                <TableHeader><TableRow>
                  <TableHead>When</TableHead><TableHead>Actor</TableHead><TableHead>Action</TableHead><TableHead>Target</TableHead>
                </TableRow></TableHeader>
                <TableBody>
                  {audit.map((a, i) => (
                    <TableRow key={i}>
                      <TableCell className="text-muted-foreground">{a.at}</TableCell>
                      <TableCell className="font-medium">{a.actor}</TableCell>
                      <TableCell>{a.action}</TableCell>
                      <TableCell className="text-muted-foreground">{a.target}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <p className="mt-3 text-xs text-muted-foreground">Placeholder — full audit trail will populate as activity accrues.</p>
          </CardContent></Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
