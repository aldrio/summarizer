import { createFileRoute, Link, Outlet } from "@tanstack/react-router";

import { Logo } from "../../components/logo/logo";

export const Route = createFileRoute("/s/_layout")({
  component: () => (
    <div className="flex flex-col gap-8 items-center">
      <div className="py-2">
        <Link to="/">
          {/*  */}
          <h1 className="flex items-center gap-2 font-bold">
            <Logo />
            <span>Summarizer</span>
          </h1>
        </Link>
      </div>
      <Outlet />
    </div>
  ),
});
