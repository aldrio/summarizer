import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { TbArrowRight } from "react-icons/tb";

import { Logo } from "../components/logo/logo";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");

  return (
    <div className="w-full min-h-screen flex flex-col justify-center items-center gap-8 bg-gradient-to-t from-slate-200 to-white">
      {/* header */}
      <div className="flex flex-col items-center gap-4">
        <Link to="/">
          {/*  */}
          <h1 className="flex items-center gap-4 text-5xl sm:text-7xl font-bold">
            <Logo />
            <span>Summarizer</span>
          </h1>
        </Link>
        <div className="text-lg sm:text-2xl italic text-slate-500">
          <span>Summarize youtube videos and articles</span>
        </div>
      </div>
      <form
        onSubmit={() =>
          navigate({
            to: "/s/$",
            params: { _splat: url.replace(/^https?:\/\//i, "") },
          })
        }
        className="px-4 flex gap-4 w-full justify-center items-center focus-within:max-w-2xl max-w-xl transition-[max-width] duration-300 ease-in-out"
      >
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste a link here"
          className="p-2 px-4 rounded-md shadow-md border grow"
          type="url"
          required
        />
        <button
          type="submit"
          className="p-2 px-4 font-medium rounded-md shadow-md bg-green bg-primary-700 hover:bg-primary-800 active:bg-primary-900 text-white flex flex-row items-center gap-2"
        >
          Summarize
          <TbArrowRight />
        </button>
      </form>

      <div>
        <p className="text-slate-600">
          By{" "}
          <a
            href="https://www.aldr.io"
            target="_blank"
            className="underline font-bold hover:text-primary-800"
          >
            Brandon Aldrich
          </a>
        </p>
      </div>
    </div>
  );
}
