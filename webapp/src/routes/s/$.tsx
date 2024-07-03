import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";

import { summarizeOptions } from "../../queries/summarize";

export const Route = createFileRoute("/s/$")({
  component: SummarizedRoute,
  loaderDeps: ({ search }) => ({ search }),
  loader: ({ context, params: { _splat: url }, deps: { search } }) => {
    // remove http or https from the url
    const urlWithoutScheme = url.replace(/https?:\/\//, "");

    // rebuild the requested url from params and search
    const fullUrl = new URL(`https://${urlWithoutScheme}`);
    fullUrl.search = new URLSearchParams(search).toString();
    console.log(fullUrl.href);
    return context.queryClient.ensureQueryData(summarizeOptions(fullUrl.href));
  },
});

function SummarizedRoute() {
  const { _splat: url } = Route.useParams();
  const summarizeQuery = useSuspenseQuery(summarizeOptions(url));

  return <data>Loaded: {JSON.stringify(summarizeQuery.data)}</data>;
}
