import { TbActivityHeartbeat } from "react-icons/tb";

import { cn } from "../../utils/cn";

export interface AlgorithmBadgeProps {
  algorithm: string;
  reductionRatio: number;
  warning?: string;
  className?: string;
}

export function AlgorithmBadge({
  algorithm,
  reductionRatio,
  warning,
  className,
}: AlgorithmBadgeProps) {
  let link: string | null = null;

  if (algorithm === "LLM") {
    link = "https://en.wikipedia.org/wiki/Large_language_model";
  } else if (algorithm === "LSA") {
    link = "https://en.wikipedia.org/wiki/Latent_semantic_analysis";
  } else if (algorithm === "TF-IDF") {
    link = "https://en.wikipedia.org/wiki/Tf%E2%80%93idf";
  } else if (algorithm === "Sentence Embeddings") {
    link =
      "https://huggingface.co/sentence-transformers/paraphrase-albert-small-v2";
  }

  return (
    <div
      className={cn(
        "text-slate-500 flex flex-row gap-2 items-start",
        className
      )}
    >
      <div className="rounded-full bg-primary-300 text-slate-600 p-1">
        <TbActivityHeartbeat />
      </div>
      <div className="flex flex-col gap-2">
        {link ? (
          <a
            href={link}
            target="_blank"
            rel="noreferrer"
            className="hover:text-slate-600"
          >
            Summarized by <span className="underline">{algorithm}</span>
          </a>
        ) : (
          <>Summarized by {algorithm}</>
        )}
        <span className="text-slate-500 text-sm">
          {reductionRatio.toFixed(2)}x reduction
        </span>
        {warning && (
          <span className="text-slate-500 text-sm italic">{warning}</span>
        )}
      </div>
    </div>
  );
}
