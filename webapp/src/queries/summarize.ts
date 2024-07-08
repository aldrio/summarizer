import { queryOptions } from "@tanstack/react-query";

import { apiFetch } from "./common";

export interface SummarizationCommon {
  url: string;
  icon: string;
  title: string;
  algorithm: string;
  reductionRatio: number;
}

export interface VideoSummarization extends SummarizationCommon {
  type: "video";
  summary: {
    start: number;
    end: number;
    text: string;
  }[];
  goodSubtitles: boolean;
}

export interface ArticleSummarization extends SummarizationCommon {
  type: "article";
  image: string | null;
  summary: string[][];
}

/**
 * Possible responses from the summarization API
 */
export type SummarizeResponse = VideoSummarization | ArticleSummarization;

export function summarizeOptions(url: string) {
  return queryOptions({
    queryKey: ["summarization", url],
    queryFn: () =>
      apiFetch<SummarizeResponse>(`summarize?url=${encodeURIComponent(url)}`),
  });
}
