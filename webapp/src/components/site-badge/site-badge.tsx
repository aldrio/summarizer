export interface SiteBadgeProps {
  url: string;
  icon: string;
  className?: string;
}

export function SiteBadge({ url, icon, className }: SiteBadgeProps) {
  return (
    <div className={className}>
      <a
        className="flex flex-row items-center font-medium gap-2 text-slate-500 hover:text-slate-600"
        href={url}
        target="_blank"
        rel="noreferrer"
      >
        <img src={icon} className="h-5" />
        <span>{new URL(url).hostname.replace(/^www\./i, "")}</span>
      </a>
    </div>
  );
}
