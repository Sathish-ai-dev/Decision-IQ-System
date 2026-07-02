import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, EmptyState } from "@/components/common/EmptyState";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import {
  Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious,
} from "@/components/ui/pagination";
import { Upload, Search, FileText, MoreHorizontal } from "lucide-react";
import { useState } from "react";
import { Button as B } from "@/components/ui/button";

export const Route = createFileRoute("/_authenticated/documents")({
  head: () => ({ meta: [{ title: "Documents — Decision IQ" }] }),
  component: DocumentsPage,
});

const initialDocs = [
  { name: "Annual Report FY25.pdf", type: "PDF", size: "3.2 MB", status: "active", updated: "2 min ago" },
  { name: "Citizen Feedback Q3.csv", type: "CSV", size: "812 KB", status: "processing", updated: "12 min ago" },
  { name: "Vendor Contracts.zip", type: "ZIP", size: "24 MB", status: "active", updated: "1 hr ago" },
  { name: "Policy Draft v3.docx", type: "DOCX", size: "142 KB", status: "draft", updated: "yesterday" },
  { name: "Budget Model.xlsx", type: "XLSX", size: "5.1 MB", status: "active", updated: "3 days ago" },
];

function DocumentsPage() {
  const [docs] = useState(initialDocs);
  return (
    <div className="space-y-6">
      <PageHeader
        title="Documents"
        description="Upload, organize, and manage documents across your projects."
        actions={<Button><Upload className="mr-1.5 h-4 w-4" /> Upload document</Button>}
      />
      <Card className="shadow-elev-1">
        <CardContent className="p-5">
          <div className="flex items-center justify-between gap-3">
            <div className="relative w-full sm:max-w-xs">
              <Search className="pointer-events-none absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Search documents..." className="pl-8" />
            </div>
            <B variant="outline" size="sm">Filters</B>
          </div>
          {docs.length === 0 ? (
            <EmptyState icon={FileText} title="No documents yet" description="Upload your first document to get started." action={<Button><Upload className="mr-1.5 h-4 w-4" /> Upload</Button>} />
          ) : (
            <>
              <div className="mt-4 overflow-hidden rounded-lg border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Size</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Updated</TableHead>
                      <TableHead className="w-10"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {docs.map((d) => (
                      <TableRow key={d.name}>
                        <TableCell className="font-medium">
                          <div className="flex items-center gap-2">
                            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
                              <FileText className="h-3.5 w-3.5" />
                            </div>
                            {d.name}
                          </div>
                        </TableCell>
                        <TableCell className="text-muted-foreground">{d.type}</TableCell>
                        <TableCell className="text-muted-foreground">{d.size}</TableCell>
                        <TableCell><StatusBadge status={d.status} /></TableCell>
                        <TableCell className="text-muted-foreground">{d.updated}</TableCell>
                        <TableCell><B variant="ghost" size="icon" aria-label="More"><MoreHorizontal className="h-4 w-4" /></B></TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
              <div className="mt-4">
                <Pagination>
                  <PaginationContent>
                    <PaginationItem><PaginationPrevious href="#" /></PaginationItem>
                    <PaginationItem><PaginationLink href="#" isActive>1</PaginationLink></PaginationItem>
                    <PaginationItem><PaginationLink href="#">2</PaginationLink></PaginationItem>
                    <PaginationItem><PaginationLink href="#">3</PaginationLink></PaginationItem>
                    <PaginationItem><PaginationNext href="#" /></PaginationItem>
                  </PaginationContent>
                </Pagination>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
