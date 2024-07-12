import Plausible from "plausible-tracker";

export type AnalyticsProperties = Record<string, string | number | boolean>;

let plausible: ReturnType<typeof Plausible> | null = null;

if (import.meta.env.PROD && import.meta.env.SSR === false) {
  plausible = Plausible({
    domain: "summarizer.aldr.io",
  });

  plausible.enableAutoPageviews();
}
