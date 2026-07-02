import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/common/EmptyState";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useTheme } from "@/contexts/ThemeProvider";
import { KeyRound, Plus, Copy } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/_authenticated/settings")({
  head: () => ({ meta: [{ title: "Settings — Decision IQ" }] }),
  component: SettingsPage,
});

function SettingsPage() {
  const { theme, setTheme } = useTheme();
  return (
    <div className="space-y-6">
      <PageHeader title="Settings" description="Manage your account, security, and workspace preferences." />
      <Tabs defaultValue="profile">
        <TabsList className="flex flex-wrap">
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="appearance">Appearance</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="organization">Organization</TabsTrigger>
          <TabsTrigger value="api">API Keys</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="grid gap-4 p-6 sm:grid-cols-2">
            <div className="space-y-1.5"><Label>Display name</Label><Input placeholder="Your name" /></div>
            <div className="space-y-1.5"><Label>Timezone</Label>
              <Select defaultValue="utc"><SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="utc">UTC</SelectItem>
                  <SelectItem value="pst">Pacific</SelectItem>
                  <SelectItem value="est">Eastern</SelectItem>
                  <SelectItem value="cet">CET</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="sm:col-span-2"><Button>Save changes</Button></div>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="security" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="grid gap-4 p-6">
            <div className="flex items-center justify-between rounded-lg border p-4">
              <div>
                <p className="text-sm font-medium">Two-factor authentication</p>
                <p className="text-xs text-muted-foreground">Add an extra layer of security to your account</p>
              </div>
              <Switch />
            </div>
            <div className="flex items-center justify-between rounded-lg border p-4">
              <div>
                <p className="text-sm font-medium">Session timeout</p>
                <p className="text-xs text-muted-foreground">Automatically sign out after inactivity</p>
              </div>
              <Select defaultValue="60">
                <SelectTrigger className="w-32"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="30">30 min</SelectItem>
                  <SelectItem value="60">1 hour</SelectItem>
                  <SelectItem value="240">4 hours</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button variant="outline">Change password</Button>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="appearance" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="grid gap-4 p-6">
            <div>
              <Label>Theme</Label>
              <p className="text-xs text-muted-foreground">Choose Light, Dark, or follow your system preference</p>
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                {(["light", "dark", "system"] as const).map((t) => (
                  <button
                    key={t}
                    onClick={() => setTheme(t)}
                    className={`rounded-lg border p-4 text-left transition-colors ${theme === t ? "border-primary bg-primary/5" : "hover:bg-accent"}`}
                  >
                    <p className="text-sm font-medium capitalize">{t}</p>
                    <p className="text-xs text-muted-foreground">
                      {t === "system" ? "Follow OS preference" : `Always ${t}`}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="notifications" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="grid gap-2 p-6">
            {[
              "Email digest",
              "Product announcements",
              "AI insight alerts",
              "Automation failures",
              "Team activity",
            ].map((k) => (
              <div key={k} className="flex items-center justify-between rounded-lg border p-4">
                <p className="text-sm">{k}</p>
                <Switch defaultChecked />
              </div>
            ))}
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="organization" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="grid gap-4 p-6 sm:grid-cols-2">
            <div className="space-y-1.5"><Label>Organization name</Label><Input placeholder="Acme Inc." /></div>
            <div className="space-y-1.5"><Label>Default role for new members</Label>
              <Select defaultValue="community"><SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="citizen">Citizen</SelectItem>
                  <SelectItem value="community">Community</SelectItem>
                  <SelectItem value="analyst">Analyst</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="sm:col-span-2"><Button>Save changes</Button></div>
          </CardContent></Card>
        </TabsContent>

        <TabsContent value="api" className="mt-4">
          <Card className="shadow-elev-1"><CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold">API Keys</p>
                <p className="text-xs text-muted-foreground">Create keys to integrate with the Decision IQ API</p>
              </div>
              <Button><Plus className="mr-1.5 h-4 w-4" /> Generate key</Button>
            </div>
            <div className="mt-4 space-y-2">
              {[{ name: "Production", val: "sk_live_••••••3f21" }, { name: "Staging", val: "sk_test_••••••9a12" }].map((k) => (
                <div key={k.name} className="flex items-center justify-between rounded-lg border p-3">
                  <div className="flex items-center gap-3">
                    <KeyRound className="h-4 w-4 text-primary" />
                    <div>
                      <p className="text-sm font-medium">{k.name}</p>
                      <p className="text-xs text-muted-foreground">{k.val}</p>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm" onClick={() => toast.success("Copied")}>
                    <Copy className="mr-1 h-3.5 w-3.5" /> Copy
                  </Button>
                </div>
              ))}
            </div>
            <p className="mt-4 text-xs text-muted-foreground">Placeholder — API access will ship with the FastAPI layer.</p>
          </CardContent></Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
