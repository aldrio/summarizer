import { createFileRoute, Link, useLocation } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { HashLoader } from "react-spinners";
import { TbArrowLeft, TbExclamationCircle } from "react-icons/tb";

import { summarizeOptions } from "../../../queries/summarize";
import { normalizeUrl } from "../../../utils/normalize";
import { ArticleSummary } from "../../../components/summary/article";
import { VideoSummary } from "../../../components/summary/video";

export const Route = createFileRoute("/s/_layout/$")({
  component: SummarizedRoute,
  pendingComponent: SummarizedRoutePending,
  loaderDeps: ({ search }) => ({ search }),
  loader: ({
    context,
    params: { _splat: url },
    deps: { search },
    location,
  }) => {
    // rebuild the requested url from params and search
    const fullUrl = new URL(normalizeUrl(url));
    fullUrl.search = new URLSearchParams(search).toString();
    fullUrl.hash = location.hash;
    return context.queryClient.ensureQueryData(summarizeOptions(fullUrl.href));
  },
  errorComponent: ({ error }) => (
    <div className="flex flex-col items-center gap-4 pt-16">
      <TbExclamationCircle className="text-red-500 text-4xl" />
      <span className="text-red-500 italic">Uh oh! {error.message}</span>
      <div className="my-16">
        <Link
          to="/"
          className="p-2 px-4 font-medium rounded-md shadow-md bg-green bg-primary-700 hover:bg-primary-800 active:bg-primary-900 text-white flex flex-row items-center gap-2"
        >
          <TbArrowLeft />
          <span>Try another</span>
        </Link>
      </div>
    </div>
  ),
});

function SummarizedRoute() {
  const { _splat: url } = Route.useParams();
  const fullUrl = new URL(normalizeUrl(url));
  fullUrl.search = new URLSearchParams(Route.useLoaderDeps().search).toString();
  fullUrl.hash = useLocation().hash;
  const { data: summary } = useSuspenseQuery(summarizeOptions(fullUrl.href));

  return (
    <div className="w-full h-full-screen flex flex-col items-center pb-8">
      {summary.type === "article" && <ArticleSummary summary={summary} />}
      {summary.type === "video" && <VideoSummary summary={summary} />}

      <div className="my-16">
        <Link
          to="/"
          className="p-2 px-4 font-medium rounded-md shadow-md bg-green bg-primary-700 hover:bg-primary-800 active:bg-primary-900 text-white flex flex-row items-center gap-2"
        >
          <TbArrowLeft />
          <span>Summarize another</span>
        </Link>
      </div>
    </div>
  );
}

function SummarizedRoutePending() {
  return (
    <div className="min-h-[200px] flex flex-col gap-8 items-center justify-center">
      <HashLoader color="rgb(152 156 188)" />
      <span className="text-slate-500 italic">
        Summarizing content. This can take a minute.
      </span>
    </div>
  );
}
