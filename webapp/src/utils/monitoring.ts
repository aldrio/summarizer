if (import.meta.env.PROD && import.meta.env.SSR === false) {
  const Sentry = await import("@sentry/react");
  Sentry.init({
    dsn: "https://3b863adc28655f68ce8832a4f747668b@o555244.ingest.us.sentry.io/4507589829394432",
    integrations: [],
    replaysSessionSampleRate: 0.0,
    replaysOnErrorSampleRate: 1.0,
  });
}
