import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Sparkles, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";
import { lovable } from "@/integrations/lovable/index";

const authSearchSchema = z.object({
  tab: z.enum(["login", "register", "forgot"]).optional(),
});

export const Route = createFileRoute("/auth")({
  validateSearch: authSearchSchema,
  head: () => ({
    meta: [
      { title: "Sign in — Decision Intelligence Platform" },
      { name: "description", content: "Sign in or create an account to access the Decision Intelligence Platform." },
    ],
  }),
  component: AuthPage,
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6, "At least 6 characters"),
  remember: z.boolean().optional(),
});

const registerSchema = z
  .object({
    fullName: z.string().min(2, "Enter your name"),
    email: z.string().email(),
    password: z.string().min(8, "At least 8 characters"),
    confirmPassword: z.string(),
    organization: z.string().optional(),
    role: z.enum(["citizen", "community", "organization", "analyst"]).default("citizen"),
  })
  .refine((v) => v.password === v.confirmPassword, {
    path: ["confirmPassword"],
    message: "Passwords do not match",
  });

const forgotSchema = z.object({ email: z.string().email() });

function AuthPage() {
  const search = Route.useSearch();
  const initialTab = search.tab ?? "login";
  const [tab, setTab] = useState<"login" | "register" | "forgot">(initialTab);

  return (
    <div className="flex min-h-screen bg-background">
      <div className="hidden flex-1 flex-col justify-between bg-gradient-to-br from-primary to-primary/70 p-12 text-primary-foreground lg:flex">
        <Link to="/" className="flex items-center gap-2 text-sm font-semibold">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary-foreground/15 backdrop-blur">
            <Sparkles className="h-4 w-4" />
          </div>
          Decision IQ
        </Link>
        <div className="max-w-md">
          <h2 className="text-3xl font-semibold tracking-tight">Decisions, grounded in your data.</h2>
          <p className="mt-3 text-primary-foreground/85">
            An enterprise AI platform trusted by citizens, organizations, and governments to decide with clarity.
          </p>
        </div>
        <p className="text-xs text-primary-foreground/70">© {new Date().getFullYear()} Decision Intelligence Platform</p>
      </div>

      <div className="flex flex-1 items-center justify-center p-4 sm:p-8">
        <div className="w-full max-w-md">
          <div className="mb-6 text-center lg:hidden">
            <Link to="/" className="inline-flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
                <Sparkles className="h-4 w-4" />
              </div>
              <span className="text-sm font-semibold">Decision IQ</span>
            </Link>
          </div>
          <Card className="shadow-elev-3">
            <CardContent className="p-6">
              <Tabs value={tab} onValueChange={(v) => setTab(v as typeof tab)}>
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="login">Sign in</TabsTrigger>
                  <TabsTrigger value="register">Register</TabsTrigger>
                  <TabsTrigger value="forgot">Forgot</TabsTrigger>
                </TabsList>
                <TabsContent value="login" className="mt-6"><LoginForm /></TabsContent>
                <TabsContent value="register" className="mt-6"><RegisterForm onSuccess={() => setTab("login")} /></TabsContent>
                <TabsContent value="forgot" className="mt-6"><ForgotForm /></TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

function LoginForm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const form = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "", remember: true },
  });

  const onSubmit = form.handleSubmit(async (values) => {
    setLoading(true);
    const { error } = await supabase.auth.signInWithPassword({
      email: values.email,
      password: values.password,
    });
    setLoading(false);
    if (error) {
      toast.error(error.message);
      return;
    }
    toast.success("Welcome back");
    navigate({ to: "/dashboard" });
  });

  const handleGoogle = async () => {
    setGoogleLoading(true);
    const result = await lovable.auth.signInWithOAuth("google", {
      redirect_uri: window.location.origin,
    });
    if (result.error) {
      toast.error("Google sign-in failed");
      setGoogleLoading(false);
      return;
    }
    if (result.redirected) return;
    navigate({ to: "/dashboard" });
  };

  return (
    <div>
      <h1 className="text-xl font-semibold tracking-tight">Welcome back</h1>
      <p className="mt-1 text-sm text-muted-foreground">Sign in to your workspace</p>
      <form onSubmit={onSubmit} className="mt-5 space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" autoComplete="email" {...form.register("email")} />
          {form.formState.errors.email && <p className="text-xs text-destructive">{form.formState.errors.email.message}</p>}
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" autoComplete="current-password" {...form.register("password")} />
          {form.formState.errors.password && <p className="text-xs text-destructive">{form.formState.errors.password.message}</p>}
        </div>
        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2 text-sm">
            <Checkbox
              checked={form.watch("remember")}
              onCheckedChange={(c) => form.setValue("remember", Boolean(c))}
            />
            Remember me
          </label>
          <button type="button" onClick={() => (document.querySelector('[value="forgot"]') as HTMLElement)?.click()} className="text-sm font-medium text-primary hover:underline">
            Forgot password?
          </button>
        </div>
        <Button type="submit" className="w-full" disabled={loading}>
          {loading && <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />} Sign in
        </Button>
      </form>
      <div className="relative my-6">
        <Separator />
        <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-card px-2 text-xs text-muted-foreground">
          OR CONTINUE WITH
        </span>
      </div>
      <Button type="button" variant="outline" className="w-full" onClick={handleGoogle} disabled={googleLoading}>
        {googleLoading ? <Loader2 className="mr-1.5 h-4 w-4 animate-spin" /> : <GoogleIcon />}
        Continue with Google
      </Button>
      <p className="mt-5 text-center text-sm text-muted-foreground">
        Don't have an account?{" "}
        <button type="button" onClick={() => (document.querySelector('[value="register"]') as HTMLElement)?.click()} className="font-medium text-primary hover:underline">
          Create one
        </button>
      </p>
    </div>
  );
}

function RegisterForm({ onSuccess }: { onSuccess: () => void }) {
  const [loading, setLoading] = useState(false);
  const form = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: { fullName: "", email: "", password: "", confirmPassword: "", organization: "", role: "citizen" as const },
  });

  const onSubmit = form.handleSubmit(async (values) => {
    setLoading(true);
    const { error } = await supabase.auth.signUp({
      email: values.email,
      password: values.password,
      options: {
        emailRedirectTo: window.location.origin,
        data: { full_name: values.fullName, organization: values.organization, requested_role: values.role },
      },
    });
    setLoading(false);
    if (error) {
      toast.error(error.message);
      return;
    }
    toast.success("Account created. You can sign in now.");
    onSuccess();
  });

  return (
    <div>
      <h1 className="text-xl font-semibold tracking-tight">Create your account</h1>
      <p className="mt-1 text-sm text-muted-foreground">Start deciding with confidence</p>
      <form onSubmit={onSubmit} className="mt-5 space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="fullName">Full name</Label>
          <Input id="fullName" {...form.register("fullName")} />
          {form.formState.errors.fullName && <p className="text-xs text-destructive">{form.formState.errors.fullName.message}</p>}
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="r-email">Email</Label>
          <Input id="r-email" type="email" {...form.register("email")} />
          {form.formState.errors.email && <p className="text-xs text-destructive">{form.formState.errors.email.message}</p>}
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-1.5">
            <Label htmlFor="r-password">Password</Label>
            <Input id="r-password" type="password" {...form.register("password")} />
            {form.formState.errors.password && <p className="text-xs text-destructive">{form.formState.errors.password.message}</p>}
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="cpassword">Confirm</Label>
            <Input id="cpassword" type="password" {...form.register("confirmPassword")} />
            {form.formState.errors.confirmPassword && <p className="text-xs text-destructive">{form.formState.errors.confirmPassword.message}</p>}
          </div>
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="org">Organization</Label>
          <Input id="org" {...form.register("organization")} placeholder="Optional" />
        </div>
        <div className="space-y-1.5">
          <Label>Role</Label>
          <Select value={form.watch("role")} onValueChange={(v) => form.setValue("role", v as never)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="citizen">Citizen</SelectItem>
              <SelectItem value="community">Community member</SelectItem>
              <SelectItem value="organization">Organization</SelectItem>
              <SelectItem value="analyst">Analyst</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <Button type="submit" className="w-full" disabled={loading}>
          {loading && <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />} Create account
        </Button>
      </form>
    </div>
  );
}

function ForgotForm() {
  const [loading, setLoading] = useState(false);
  const form = useForm({
    resolver: zodResolver(forgotSchema),
    defaultValues: { email: "" },
  });
  const onSubmit = form.handleSubmit(async (values) => {
    setLoading(true);
    const { error } = await supabase.auth.resetPasswordForEmail(values.email, {
      redirectTo: `${window.location.origin}/reset-password`,
    });
    setLoading(false);
    if (error) { toast.error(error.message); return; }
    toast.success("Password reset email sent");
  });

  return (
    <div>
      <h1 className="text-xl font-semibold tracking-tight">Reset your password</h1>
      <p className="mt-1 text-sm text-muted-foreground">We'll email a reset link</p>
      <form onSubmit={onSubmit} className="mt-5 space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="f-email">Email</Label>
          <Input id="f-email" type="email" {...form.register("email")} />
          {form.formState.errors.email && <p className="text-xs text-destructive">{form.formState.errors.email.message}</p>}
        </div>
        <Button type="submit" className="w-full" disabled={loading}>
          {loading && <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />} Send reset link
        </Button>
      </form>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24" aria-hidden>
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.75h3.57c2.08-1.92 3.28-4.74 3.28-8.07z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.75c-.99.66-2.25 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.12A6.98 6.98 0 0 1 5.47 12c0-.74.13-1.45.36-2.12V7.04H2.18A11 11 0 0 0 1 12c0 1.77.42 3.45 1.18 4.96l3.66-2.84z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.04l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z"/>
    </svg>
  );
}
