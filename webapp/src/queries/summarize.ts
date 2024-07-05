import { queryOptions } from "@tanstack/react-query";

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
    queryFn: async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/summarize?url=${encodeURIComponent(url)}`
      );

      if (!response.ok) {
        throw new Error("Error");
      }

      const data = await response.json();
      return data as SummarizeResponse;
    },
  });
}
