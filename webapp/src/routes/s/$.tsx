import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";

import { summarizeOptions } from "../../queries/summarize";
import { normalizeUrl } from "../../utils/normalize";

export const Route = createFileRoute("/s/$")({
  component: SummarizedRoute,
  loaderDeps: ({ search }) => ({ search }),
  loader: ({ context, params: { _splat: url }, deps: { search } }) => {
    // rebuild the requested url from params and search
    const fullUrl = new URL(normalizeUrl(url));
    fullUrl.search = new URLSearchParams(search).toString();
    return context.queryClient.ensureQueryData(summarizeOptions(fullUrl.href));
  },
});

function SummarizedRoute() {
  const { _splat: url } = Route.useParams();
  const summarizeQuery = useSuspenseQuery(summarizeOptions(url));

  return <data>Loaded: {JSON.stringify(summarizeQuery.data)}</data>;
}
