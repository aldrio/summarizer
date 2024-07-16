import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { TbArrowRight, TbChevronRight } from "react-icons/tb";

import { Logo } from "../components/logo/logo";
import { Select } from "../components/select/select";
import { useLocalStorage } from "../utils/use-localstorage";

import procrastinator from "./examples/procrastinator.jpg";
import interpreters from "./examples/interpreters.jpg";
import archeology from "./examples/archeology.jpg";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");
  const [algorithm, setAlgorithm] = useLocalStorage("algorithm", "llm");

  return (
    <div className="w-full min-h-screen flex flex-col">
      <div className="w-full grow flex flex-col justify-center items-center gap-8 pt-[20vh]">
        {/* header */}
        <div className="flex flex-col items-center gap-4">
          <Link to="/">
            {/*  */}
            <h1 className="flex items-center gap-4 text-4xl sm:text-5xl md:text-7xl font-bold">
              <Logo />
              <span>Summarizer</span>
            </h1>
          </Link>
          <div className="text-lg md:text-2xl italic text-slate-500">
            <span>Summarize youtube videos and articles</span>
          </div>
        </div>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            navigate({
              to: "/s/$",
              params: { _splat: url.replace(/^https?:\/\//i, "") },
            });
          }}
          className="px-4 flex gap-4 w-full justify-center items-center focus-within:max-w-2xl max-w-xl transition-[max-width] duration-300 ease-in-out"
        >
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste a link here"
            className="p-2 px-4 rounded-md shadow-md border grow w-full"
            type="url"
            required
          />
          <button
            type="submit"
            className="p-2 px-4 font-medium rounded-md shadow-md bg-primary-700 hover:bg-primary-800 active:bg-primary-900 text-white flex flex-row items-center gap-2"
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

        <div className="flex flex-col gap-8 items-center mt-20 mb-20 max-w-xl lg:max-w-4xl px-4 w-full">
          <div className="flex flex-row gap-2 items-center w-full">
            <div className="border-b border-slate-300 grow"></div>
            <div className="text-slate-500 text-sm ">Samples</div>
            <div className="border-b border-slate-300 grow"></div>
          </div>
          <div className="flex flex-col lg:flex-row gap-8 w-full">
            <ExampleThumbnail
              title="Inside the Mind of a Master Procrastinator | Tim Urban | TED"
              image={procrastinator}
              favicon="https://www.youtube.com/favicon.ico"
              url="https://www.youtube.com/watch?v=arj7oStGLkU"
            />
            <ExampleThumbnail
              title="How the UN Translates Everything in Real-Time"
              image={interpreters}
              favicon="https://www.youtube.com/favicon.ico"
              url="https://www.youtube.com/watch?v=0lbFEMqO_gg"
            />
            <ExampleThumbnail
              title="4,000-year-old Greek hilltop site mystifies archaeologists"
              image={archeology}
              favicon="https://apnews.com/favicon.ico"
              url="https://apnews.com/article/greece-crete-archaeology-airport-minoan-e1bca3960994b42ef2ec30676a2ae188"
            />
          </div>
        </div>
      </div>

      <Select
        className="self-end m-4"
        onChange={setAlgorithm}
        value={algorithm}
        items={[
          { key: "llm", label: "LLM" },
          { key: "tf_idf", label: "TF-IDF" },
          { key: "lsa", label: "LSA" },
        ]}
      />
    </div>
  );
}

interface ExampleThumbnailProps {
  title: string;
  url: string;
  favicon: string;
  image: string;
}

function ExampleThumbnail({
  title,
  url,
  favicon,
  image,
}: ExampleThumbnailProps) {
  return (
    <Link
      as="a"
      to="/s/$"
      params={{ _splat: url.replace(/^https?:\/\//i, "") }}
      className="shadow-lg flex flex-col flex-1 bg-white overflow-hidden rounded-lg group hover:shadow-xl transition-shadow duration-300 ease-in-out"
    >
      <div className="aspect-video bg-slate-200 overflow-hidden">
        <img
          src={image}
          alt="thumbnail"
          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500 ease-in-out"
        />
      </div>
      <div className="flex flex-row gap-4 items-center p-4">
        <div className="text-md font-medium text-slate-600 flex flex-row gap-2 items-baseline group-hover:text-slate-900 transition-colors duration-300 ease-in-out">
          <img src={favicon} className="w-4 h-4" />
          <span>{title}</span>
        </div>
        <div>
          <TbChevronRight className="text-primary-300 group-hover:text-primary-600 transition-colors duration-300 ease-in-out" />
        </div>
      </div>
    </Link>
  );
}
