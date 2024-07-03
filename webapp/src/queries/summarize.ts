import { queryOptions } from "@tanstack/react-query";

/**
 * Possible responses from the summarization API
 */
export type SummarizeResponse =
  | {
      type: "video";
      summary: string[];
      url: string;
      title: string;
      icon: string;
      goodSubtitles: boolean;
    }
  | {
      type: "article";
      summary: string[];
      url: string;
      title: string;
      icon: string;
      image: string;
    };

export function summarizeOptions(url: string) {
  return queryOptions({
    queryKey: ["summarization", url],
    queryFn: async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/summarize?url=${encodeURIComponent(url)}`,
      );

      if (!response.ok) {
        throw new Error("Error");
      }

      const data = await response.json();
      return data as SummarizeResponse;
    },
  });
}
