import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useAuth } from "@/hooks/use-auth";

export const Route = createFileRoute("/_authenticated/profile")({
  head: () => ({ meta: [{ title: "Profile — Decision IQ" }] }),
  component: ProfilePage,
});

function ProfilePage() {
  const { user } = useAuth();
  const initials = (user?.email ?? "U").split("@")[0].slice(0, 2).toUpperCase();
  return (
    <div className="space-y-6">
      <PageHeader title="Profile" description="Manage how you appear across the platform." />
      <Card className="shadow-elev-1">
        <CardContent className="p-6">
          <div className="flex items-center gap-4">
            <Avatar className="h-16 w-16">
              <AvatarFallback className="bg-primary text-lg text-primary-foreground">{initials}</AvatarFallback>
            </Avatar>
            <div>
              <p className="text-lg font-semibold">{user?.email ?? "Account"}</p>
              <p className="text-sm text-muted-foreground">Citizen · Personal workspace</p>
            </div>
          </div>
          <form className="mt-6 grid gap-4 sm:grid-cols-2" onSubmit={(e) => e.preventDefault()}>
            <div className="space-y-1.5">
              <Label htmlFor="name">Full name</Label>
              <Input id="name" defaultValue="" placeholder="Your name" />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="email">Email</Label>
              <Input id="email" defaultValue={user?.email ?? ""} disabled />
            </div>
            <div className="space-y-1.5 sm:col-span-2">
              <Label htmlFor="bio">Bio</Label>
              <Textarea id="bio" rows={4} placeholder="Tell your team a little about yourself." />
            </div>
            <div className="sm:col-span-2">
              <Button>Save profile</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
