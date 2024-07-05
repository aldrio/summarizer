import { ArticleSummarization } from "../../queries/summarize";
import { AlgorithmBadge } from "../algorithm-badge/algirithm-badge";
import { SiteBadge } from "../site-badge/site-badge";

export interface ArticleSummaryProps {
  className?: string;
  summary: ArticleSummarization;
}

export function ArticleSummary({ summary }: ArticleSummaryProps) {
  const paragraphs = summary.summary;
  return (
    <div className="w-full max-w-xl px-4">
      <SiteBadge url={summary.url} icon={summary.icon} className="mb-4" />
      <h1 className="text-3xl font-bold mb-6">{summary.title}</h1>
      {summary.image && <img src={summary.image} className="w-full mb-8" />}
      {paragraphs.map((sentences, i) => (
        <p key={i} className="text-lg mb-4">
          {sentences.join(" ")}
        </p>
      ))}
      <AlgorithmBadge
        algorithm={summary.algorithm}
        reductionRatio={summary.reductionRatio}
        className="mt-6"
      />
    </div>
  );
}
