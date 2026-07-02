import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { PageHeader } from "@/components/common/EmptyState";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Upload, FolderKanban } from "lucide-react";

export const Route = createFileRoute("/_authenticated/datasets")({
  head: () => ({ meta: [{ title: "Datasets — Decision IQ" }] }),
  component: DatasetsPage,
});

const datasets = [
  { name: "Sales 2024", category: "Sales", rows: "812K", status: "active" },
  { name: "Citizen Feedback", category: "Survey", rows: "42K", status: "processing" },
  { name: "Vendor Spend", category: "Finance", rows: "6.2K", status: "active" },
  { name: "Support Tickets", category: "Ops", rows: "18K", status: "active" },
  { name: "Fleet Telemetry", category: "IoT", rows: "2.1M", status: "syncing" },
  { name: "Legacy Archive", category: "Archive", rows: "—", status: "archived" },
];

function DatasetsPage() {
  const [view, setView] = useState<"grid" | "table">("grid");
  return (
    <div className="space-y-6">
      <PageHeader
        title="Datasets"
        description="Curated tables ready for analysis, insights, and AI grounding."
        actions={<Button><Upload className="mr-1.5 h-4 w-4" /> Upload dataset</Button>}
      />
      <Card className="shadow-elev-1">
        <CardContent className="p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <Tabs value={view} onValueChange={(v) => setView(v as "grid" | "table")}>
              <TabsList>
                <TabsTrigger value="grid">Grid</TabsTrigger>
                <TabsTrigger value="table">Table</TabsTrigger>
              </TabsList>
            </Tabs>
            <Select defaultValue="all">
              <SelectTrigger className="sm:w-40"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All categories</SelectItem>
                <SelectItem value="sales">Sales</SelectItem>
                <SelectItem value="finance">Finance</SelectItem>
                <SelectItem value="ops">Operations</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Tabs value={view} className="mt-4">
            <TabsContent value="grid">
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {datasets.map((d) => (
                  <Card key={d.name} className="shadow-elev-1">
                    <CardContent className="p-5">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                          <FolderKanban className="h-4 w-4" />
                        </div>
                        <StatusBadge status={d.status} />
                      </div>
                      <h3 className="mt-3 text-sm font-semibold">{d.name}</h3>
                      <p className="mt-1 text-xs text-muted-foreground">{d.category} · {d.rows} rows</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
            <TabsContent value="table">
              <div className="overflow-hidden rounded-lg border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead>Rows</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {datasets.map((d) => (
                      <TableRow key={d.name}>
                        <TableCell className="font-medium">{d.name}</TableCell>
                        <TableCell className="text-muted-foreground">{d.category}</TableCell>
                        <TableCell>{d.rows}</TableCell>
                        <TableCell><StatusBadge status={d.status} /></TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
