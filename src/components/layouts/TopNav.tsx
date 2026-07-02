import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { Bell, LogOut, Search, User as UserIcon, Settings as SettingsIcon } from "lucide-react";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/hooks/use-auth";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { NAV_GROUPS } from "@/constants/navigation";

function useBreadcrumb() {
  const pathname = useRouterState({ select: (r) => r.location.pathname });
  for (const g of NAV_GROUPS) {
    for (const item of g.items) {
      if (item.url === pathname) return { group: g.label, page: item.title };
    }
  }
  if (pathname === "/profile") return { group: "Account", page: "Profile" };
  return { group: "Overview", page: "Dashboard" };
}

export function TopNav() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { group, page } = useBreadcrumb();

  const initials = (user?.email ?? "U")
    .split("@")[0]
    .slice(0, 2)
    .toUpperCase();

  const handleSignOut = async () => {
    await queryClient.cancelQueries();
    queryClient.clear();
    await supabase.auth.signOut();
    toast.success("Signed out");
    navigate({ to: "/auth", replace: true });
  };

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b bg-background/80 px-3 backdrop-blur sm:px-4">
      <SidebarTrigger className="-ml-1" />
      <div className="hidden text-sm text-muted-foreground sm:flex sm:items-center sm:gap-1.5">
        <span>{group}</span>
        <span className="text-muted-foreground/50">/</span>
        <span className="font-medium text-foreground">{page}</span>
      </div>
      <div className="ml-auto flex items-center gap-1.5">
        <div className="relative hidden md:block">
          <Search className="pointer-events-none absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search..."
            className="w-56 pl-8 lg:w-72"
            aria-label="Search platform"
          />
        </div>
        <Button variant="ghost" size="icon" aria-label="Notifications" asChild>
          <Link to="/notifications">
            <Bell className="h-4 w-4" />
          </Link>
        </Button>
        <ThemeToggle />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-9 gap-2 pl-1.5 pr-2">
              <Avatar className="h-7 w-7">
                <AvatarFallback className="bg-primary text-xs text-primary-foreground">
                  {initials}
                </AvatarFallback>
              </Avatar>
              <span className="hidden max-w-[10rem] truncate text-sm sm:inline">
                {user?.email ?? "Account"}
              </span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel className="truncate">{user?.email}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link to="/profile"><UserIcon className="mr-2 h-4 w-4" /> Profile</Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link to="/settings"><SettingsIcon className="mr-2 h-4 w-4" /> Settings</Link>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleSignOut}>
              <LogOut className="mr-2 h-4 w-4" /> Sign out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
