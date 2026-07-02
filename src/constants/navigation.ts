import {
  LayoutDashboard,
  Sparkles,
  Lightbulb,
  Database,
  FileText,
  FolderKanban,
  BarChart3,
  FileBarChart,
  Workflow,
  Building2,
  Users,
  Bell,
  Settings,
  ShieldCheck,
  type LucideIcon,
} from "lucide-react";

export interface NavItem {
  title: string;
  url: string;
  icon: LucideIcon;
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}

export const NAV_GROUPS: NavGroup[] = [
  {
    label: "Overview",
    items: [{ title: "Dashboard", url: "/dashboard", icon: LayoutDashboard }],
  },
  {
    label: "AI",
    items: [
      { title: "AI Assistant", url: "/ai-assistant", icon: Sparkles },
      { title: "Insights", url: "/insights", icon: Lightbulb },
    ],
  },
  {
    label: "Data",
    items: [
      { title: "Data Sources", url: "/data-sources", icon: Database },
      { title: "Documents", url: "/documents", icon: FileText },
      { title: "Datasets", url: "/datasets", icon: FolderKanban },
    ],
  },
  {
    label: "Analytics",
    items: [
      { title: "Analytics", url: "/analytics", icon: BarChart3 },
      { title: "Reports", url: "/reports", icon: FileBarChart },
    ],
  },
  {
    label: "Automation",
    items: [{ title: "Automation", url: "/automation", icon: Workflow }],
  },
  {
    label: "Administration",
    items: [
      { title: "Organizations", url: "/organizations", icon: Building2 },
      { title: "Users", url: "/users", icon: Users },
      { title: "Notifications", url: "/notifications", icon: Bell },
      { title: "Settings", url: "/settings", icon: Settings },
      { title: "Admin", url: "/admin", icon: ShieldCheck },
    ],
  },
];
