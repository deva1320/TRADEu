"use client";

import { useEffect, useState } from "react";

type ApiStatus = {
  status: string;
  service: string;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export default function Home() {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkApi = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`${API_BASE_URL}/health`, {
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }

        const data: ApiStatus = await response.json();
        setApiStatus(data);
      } catch {
        setApiStatus(null);
        setError("Unable to connect to TRADEu API");
      } finally {
        setLoading(false);
      }
    };

    checkApi();
  }, []);

  const isOnline = apiStatus?.status === "healthy";

  return (
    <main className="min-h-screen bg-[#070b14] text-white">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-8 lg:px-10">
        <header className="flex items-center justify-between border-b border-white/10 pb-6">
          <div>
            <div className="text-2xl font-bold tracking-tight">
              TRADE<span className="text-cyan-400">u</span>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              AI-Powered Indian Trading and Investing Intelligence
            </p>
          </div>

          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs text-slate-300">
            Development Environment
          </div>
        </header>

        <section className="flex flex-1 items-center py-16">
          <div className="grid w-full gap-10 lg:grid-cols-[1.3fr_0.7fr] lg:items-center">
            <div>
              <div className="mb-5 inline-flex rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-300">
                TRADEu Platform Foundation
              </div>

              <h1 className="max-w-3xl text-5xl font-bold leading-tight tracking-tight sm:text-6xl">
                Intelligent market analysis,
                <span className="block text-cyan-400">
                  built for Indian markets.
                </span>
              </h1>

              <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
                TRADEu combines real-time market data, technical analysis,
                price action, strategy intelligence, risk management and AI
                decision support in one platform.
              </p>

              <div className="mt-8 flex flex-wrap gap-3">
                {[
                  "Real-Time Market Data",
                  "Technical Analysis",
                  "Price Action",
                  "AI Intelligence",
                ].map((feature) => (
                  <span
                    key={feature}
                    className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300"
                  >
                    {feature}
                  </span>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6 shadow-2xl">
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-400">System Status</p>
                  <h2 className="mt-1 text-xl font-semibold">
                    TRADEu Backend
                  </h2>
                </div>

                <div
                  className={`h-3 w-3 rounded-full ${
                    loading
                      ? "bg-yellow-400"
                      : isOnline
                        ? "bg-emerald-400"
                        : "bg-red-400"
                  }`}
                />
              </div>

              <div className="space-y-4">
                <div className="rounded-xl border border-white/10 bg-black/20 p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-400">
                      FastAPI Server
                    </span>

                    <span
                      className={`text-sm font-medium ${
                        loading
                          ? "text-yellow-400"
                          : isOnline
                            ? "text-emerald-400"
                            : "text-red-400"
                      }`}
                    >
                      {loading
                        ? "Checking..."
                        : isOnline
                          ? "Online"
                          : "Offline"}
                    </span>
                  </div>

                  <p className="mt-2 text-xs text-slate-500">
                    {API_BASE_URL}
                  </p>
                </div>

                <div className="rounded-xl border border-white/10 bg-black/20 p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-400">
                      API Service
                    </span>

                    <span className="text-sm text-slate-200">
                      {apiStatus?.service ?? "tradeu-api"}
                    </span>
                  </div>
                </div>

                <div className="rounded-xl border border-white/10 bg-black/20 p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-400">
                      Connection
                    </span>

                    <span className="text-sm text-slate-200">
                      {error ? error : "Frontend to Backend"}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <footer className="border-t border-white/10 pt-5 text-xs text-slate-500">
          TRADEu - Design System Foundation - Phase 5
        </footer>
      </div>
    </main>
  );
}
