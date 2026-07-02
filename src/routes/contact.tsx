import { createFileRoute } from "@tanstack/react-router";
import { MarketingShell } from "@/components/layouts/MarketingShell";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Mail, MapPin, Phone } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/contact")({
  head: () => ({
    meta: [
      { title: "Contact — Decision Intelligence Platform" },
      { name: "description", content: "Get in touch with the Decision Intelligence Platform team." },
    ],
  }),
  component: ContactPage,
});

function ContactPage() {
  return (
    <MarketingShell>
      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-semibold tracking-tight">Contact us</h1>
          <p className="mt-3 text-muted-foreground">
            Tell us about your organization and how we can help you decide better.
          </p>
        </div>
        <div className="mt-12 grid gap-8 lg:grid-cols-3">
          <div className="space-y-4 lg:col-span-1">
            {[
              { icon: Mail, label: "Email", value: "hello@decisioniq.example" },
              { icon: Phone, label: "Phone", value: "+1 (555) 010-2024" },
              { icon: MapPin, label: "Address", value: "1600 Innovation Way, Mountain View" },
            ].map((c) => (
              <Card key={c.label} className="shadow-elev-1">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                    <c.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">{c.label}</p>
                    <p className="text-sm font-medium">{c.value}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          <Card className="shadow-elev-1 lg:col-span-2">
            <CardContent className="p-6">
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault();
                  toast.success("Message sent. We'll be in touch shortly.");
                  (e.target as HTMLFormElement).reset();
                }}
              >
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <Label htmlFor="name">Full name</Label>
                    <Input id="name" required placeholder="Jane Doe" />
                  </div>
                  <div className="space-y-1.5">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" required placeholder="jane@company.com" />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="org">Organization</Label>
                  <Input id="org" placeholder="Company or agency" />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="msg">Message</Label>
                  <Textarea id="msg" required rows={5} placeholder="How can we help?" />
                </div>
                <Button type="submit">Send message</Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>
    </MarketingShell>
  );
}
