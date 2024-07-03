import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");

  return (
    <div className="p-2">
      <form
        onSubmit={() =>
          navigate({
            to: "/s/$",
            params: { _splat: url.replace(/^https?:\/\//i, "") },
          })
        }
      >
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border border-gray-300 rounded p-1"
        />
        <button type="submit" className="border border-gray-300 rounded p-1">
          Summarize
        </button>
      </form>
    </div>
  );
}
