import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, Search, Database } from "lucide-react";

export const Route = createFileRoute("/_authenticated/data-sources")({
  head: () => ({ meta: [{ title: "Data Sources — Decision IQ" }] }),
  component: DataSourcesPage,
});

const rows = [
  { name: "Warehouse-East", type: "PostgreSQL", status: "active", last: "2 min ago", records: "1.2M" },
  { name: "Warehouse-West", type: "PostgreSQL", status: "failed", last: "4 days ago", records: "820K" },
  { name: "CRM Salesforce", type: "API", status: "active", last: "12 min ago", records: "312K" },
  { name: "S3 Documents Bucket", type: "Storage", status: "syncing", last: "just now", records: "48K" },
  { name: "BigQuery Analytics", type: "Warehouse", status: "active", last: "1 hr ago", records: "5.6M" },
  { name: "Legacy Oracle", type: "Database", status: "archived", last: "30 days ago", records: "—" },
];

function DataSourcesPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Data Sources"
        description="Connect databases, warehouses, APIs, and storage to your workspace."
        actions={<Button><Plus className="mr-1.5 h-4 w-4" /> Connect source</Button>}
      />
      <Card className="shadow-elev-1">
        <CardContent className="p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="relative w-full sm:max-w-xs">
              <Search className="pointer-events-none absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Search sources..." className="pl-8" />
            </div>
            <Select defaultValue="all">
              <SelectTrigger className="sm:w-40"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All types</SelectItem>
                <SelectItem value="db">Database</SelectItem>
                <SelectItem value="api">API</SelectItem>
                <SelectItem value="storage">Storage</SelectItem>
                <SelectItem value="warehouse">Warehouse</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="mt-4 overflow-hidden rounded-lg border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Records</TableHead>
                  <TableHead>Last synced</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((r) => (
                  <TableRow key={r.name}>
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
                          <Database className="h-3.5 w-3.5" />
                        </div>
                        {r.name}
                      </div>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{r.type}</TableCell>
                    <TableCell><StatusBadge status={r.status} /></TableCell>
                    <TableCell>{r.records}</TableCell>
                    <TableCell className="text-muted-foreground">{r.last}</TableCell>
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
