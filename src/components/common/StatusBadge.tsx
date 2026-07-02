import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type Status = "active" | "draft" | "archived" | "processing" | "failed" | "connected" | "syncing";

const map: Record<Status, string> = {
  active: "bg-success/15 text-success border-success/20",
  connected: "bg-success/15 text-success border-success/20",
  draft: "bg-muted text-muted-foreground border-border",
  archived: "bg-muted text-muted-foreground border-border",
  processing: "bg-primary/15 text-primary border-primary/20",
  syncing: "bg-primary/15 text-primary border-primary/20",
  failed: "bg-destructive/15 text-destructive border-destructive/20",
};

export function StatusBadge({ status, className }: { status: Status | string; className?: string }) {
  const key = (status.toLowerCase() as Status) in map ? (status.toLowerCase() as Status) : "draft";
  return (
    <Badge variant="outline" className={cn("font-medium capitalize", map[key], className)}>
      {status}
    </Badge>
  );
}
