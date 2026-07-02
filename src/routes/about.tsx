import { createFileRoute } from "@tanstack/react-router";
import { MarketingShell } from "@/components/layouts/MarketingShell";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "About — Decision Intelligence Platform" },
      { name: "description", content: "Our mission is to make enterprise decision intelligence accessible to every organization and citizen." },
    ],
  }),
  component: AboutPage,
});

function AboutPage() {
  return (
    <MarketingShell>
      <section className="mx-auto max-w-3xl px-4 py-20 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-semibold tracking-tight">About Decision IQ</h1>
        <p className="mt-4 text-lg text-muted-foreground">
          We build enterprise AI infrastructure that transforms fragmented data into decisions
          any team can act on with confidence.
        </p>
        <div className="prose prose-slate dark:prose-invert mt-8 max-w-none text-sm text-muted-foreground">
          <p>
            Decision intelligence sits at the crossroads of data engineering, AI, and human judgment.
            Our platform provides a single governed layer where teams can bring their data, ask
            grounded questions in natural language, and automate follow-through — all with the
            security and auditability enterprises require.
          </p>
          <h2 className="mt-8 text-xl font-semibold text-foreground">Our mission</h2>
          <p>
            Empower citizens, organizations, and government teams to make faster, better, more
            transparent decisions.
          </p>
          <h2 className="mt-8 text-xl font-semibold text-foreground">Our approach</h2>
          <p>
            We combine best-in-class open technologies — FastAPI, Google Cloud, Vertex AI, Gemini,
            LangChain, ChromaDB — into a coherent, extensible platform. Every layer is designed for
            production and governed access.
          </p>
        </div>
      </section>
    </MarketingShell>
  );
}
