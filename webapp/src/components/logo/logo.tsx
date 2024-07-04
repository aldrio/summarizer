import { SVGProps } from "react";

export interface LogoProps extends SVGProps<SVGSVGElement> {
  className?: string;
}

export function Logo(props: LogoProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      height="1em"
      width="auto"
      {...props}
    >
      <rect width="20" height="5.2" fill="#6F6F93" />
      <rect y="7.40002" width="20" height="5.2" fill="#6F6F93" />
      <rect y="14.8" width="15.4" height="5.2" fill="#6F6F93" />
    </svg>
  );
}
