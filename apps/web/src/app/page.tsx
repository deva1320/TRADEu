"use client";

import { useEffect, useState } from "react";

type ApiStatus = {
  status: string;
  service: string;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const navigation = [
  { label: "Dashboard", icon: "⌂", active: true },
  { label: "Markets", icon: "▥" },
  { label: "Charts", icon: "◫" },
  { label: "Screener", icon: "⌕" },
  { label: "Watchlist", icon: "☆" },
  { label: "News", icon: "▤" },
];

const intelligence = [
  { label: "Drishti AI", icon: "✦" },
  { label: "Strategy Builder", icon: "◇" },
  { label: "Backtesting", icon: "↗" },
];

const portfolio = [
  { label: "Paper Trading", icon: "◎" },
  { label: "Portfolio", icon: "▣" },
  { label: "Journal", icon: "≡" },
  { label: "Invest", icon: "◈" },
];

const system = [
  { label: "Alerts", icon: "♢" },
  { label: "Learn", icon: "?" },
  { label: "Settings", icon: "⚙" },
];

const marketCards = [
  {
    name: "NIFTY 50",
    value: "—",
    change: "Market data pending",
  },
  {
    name: "BANK NIFTY",
    value: "—",
    change: "Market data pending",
  },
  {
    name: "SENSEX",
    value: "—",
    change: "Market data pending",
  },
];

function NavigationSection({
  title,
  items,
}: {
  title: string;
  items: { label: string; icon: string; active?: boolean }[];
}) {
  return (
    <div className="mb-6">
      <p className="mb-2 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-600">
        {title}
      </p>

      <div className="space-y-1">
        {items.map((item) => (
          <button
            key={item.label}
            className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition ${
              item.active
                ? "bg-cyan-400/10 text-cyan-300 ring-1 ring-inset ring-cyan-400/15"
                : "text-slate-400 hover:bg-white/[0.04] hover:text-slate-200"
            }`}
          >
            <span className="flex h-6 w-6 items-center justify-center text-sm">
              {item.icon}
            </span>

            <span>{item.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default function Home() {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkApi = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/health`, {
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error("API unavailable");
        }

        const data: ApiStatus = await response.json();
        setApiStatus(data);
      } catch {
        setApiStatus(null);
      } finally {
        setLoading(false);
      }
    };

    checkApi();
  }, []);

  const isOnline = apiStatus?.status === "healthy";

  return (
    <main className="min-h-screen bg-[#070b14] text-slate-100">
      <div className="flex min-h-screen">
        {/* SIDEBAR */}
        <aside className="hidden w-64 shrink-0 border-r border-white/[0.07] bg-[#090e18] lg:flex lg:flex-col">
          <div className="flex h-16 items-center border-b border-white/[0.07] px-5">
            <div>
              <div className="text-xl font-bold tracking-tight">
                TRADE<span className="text-cyan-400">u</span>
              </div>

              <div className="mt-0.5 text-[10px] uppercase tracking-[0.16em] text-slate-600">
                Trading Intelligence
              </div>
            </div>
          </div>

          <nav className="flex-1 overflow-y-auto px-3 py-5">
            <NavigationSection title="Workspace" items={navigation} />
            <NavigationSection title="Intelligence" items={intelligence} />
            <NavigationSection title="Trading & Portfolio" items={portfolio} />
            <NavigationSection title="System" items={system} />
          </nav>

          <div className="border-t border-white/[0.07] p-4">
            <div className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-3">
              <div className="flex items-center gap-2">
                <span
                  className={`h-2 w-2 rounded-full ${
                    loading
                      ? "bg-yellow-400"
                      : isOnline
                        ? "bg-emerald-400"
                        : "bg-red-400"
                  }`}
                />

                <span className="text-xs text-slate-400">
                  {loading
                    ? "Checking system..."
                    : isOnline
                      ? "System operational"
                      : "API offline"}
                </span>
              </div>
            </div>
          </div>
        </aside>

        {/* MAIN APPLICATION */}
        <div className="flex min-w-0 flex-1 flex-col">
          {/* TOP BAR */}
          <header className="flex h-16 items-center justify-between border-b border-white/[0.07] bg-[#090e18]/90 px-5 backdrop-blur-xl lg:px-7">
            <div className="flex items-center gap-4">
              <div className="lg:hidden">
                <span className="text-lg font-bold">
                  TRADE<span className="text-cyan-400">u</span>
                </span>
              </div>

              <div className="hidden h-8 w-px bg-white/[0.08] lg:block" />

              <div>
                <p className="text-sm font-medium text-slate-200">
                  Market Overview
                </p>
                <p className="text-xs text-slate-600">
                  Indian markets intelligence workspace
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button className="hidden rounded-lg border border-white/[0.08] bg-white/[0.025] px-3 py-2 text-xs text-slate-400 sm:block">
                Search markets...
              </button>

              <button className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/[0.08] bg-white/[0.025] text-slate-400">
                ♢
              </button>

              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-cyan-400/10 text-sm font-semibold text-cyan-300 ring-1 ring-cyan-400/20">
                D
              </div>
            </div>
          </header>

          {/* CONTENT */}
          <section className="flex-1 overflow-auto">
            <div className="mx-auto max-w-[1600px] p-5 lg:p-7">
              {/* PAGE HEADER */}
              <div className="mb-7 flex flex-col justify-between gap-4 md:flex-row md:items-end">
                <div>
                  <div className="mb-2 inline-flex items-center gap-2 rounded-full border border-cyan-400/15 bg-cyan-400/[0.06] px-3 py-1.5 text-[11px] font-medium text-cyan-300">
                    <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
                    TRADEu Intelligence Platform
                  </div>

                  <h1 className="text-3xl font-semibold tracking-tight text-white lg:text-4xl">
                    Good morning, welcome back.
                  </h1>

                  <p className="mt-2 text-sm text-slate-500">
                    Your market intelligence workspace is ready.
                  </p>
                </div>

                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <span
                    className={`h-2 w-2 rounded-full ${
                      isOnline ? "bg-emerald-400" : "bg-red-400"
                    }`}
                  />
                  API {isOnline ? "Connected" : "Disconnected"}
                </div>
              </div>

              {/* MARKET CARDS */}
              <div className="mb-6 grid gap-4 md:grid-cols-3">
                {marketCards.map((market) => (
                  <div
                    key={market.name}
                    className="rounded-xl border border-white/[0.07] bg-[#0d1422] p-5 transition hover:border-white/[0.12]"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
                        {market.name}
                      </span>

                      <span className="text-xs text-slate-600">NSE</span>
                    </div>

                    <div className="mt-4 flex items-end justify-between">
                      <span className="font-mono text-2xl font-semibold text-slate-200">
                        {market.value}
                      </span>

                      <span className="text-xs text-slate-600">
                        {market.change}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* MAIN GRID */}
              <div className="grid gap-5 xl:grid-cols-[1.5fr_1fr]">
                {/* MARKET INTELLIGENCE */}
                <div className="rounded-xl border border-white/[0.07] bg-[#0d1422]">
                  <div className="flex items-center justify-between border-b border-white/[0.07] px-5 py-4">
                    <div>
                      <h2 className="text-sm font-semibold text-slate-200">
                        Market Intelligence
                      </h2>
                      <p className="mt-1 text-xs text-slate-600">
                        Real-time and historical market workspace
                      </p>
                    </div>

                    <button className="text-xs text-cyan-400">
                      Open Markets →
                    </button>
                  </div>

                  <div className="p-5">
                    <div className="flex min-h-[260px] items-center justify-center rounded-lg border border-dashed border-white/[0.08] bg-[#090e18]">
                      <div className="text-center">
                        <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-400/[0.06] text-xl text-cyan-400">
                          ◫
                        </div>

                        <p className="text-sm font-medium text-slate-300">
                          Market visualization workspace
                        </p>

                        <p className="mt-1 max-w-sm text-xs leading-5 text-slate-600">
                          Charts, indicators, price action and market
                          analytics will be connected in later phases.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* WATCHLIST */}
                <div className="rounded-xl border border-white/[0.07] bg-[#0d1422]">
                  <div className="flex items-center justify-between border-b border-white/[0.07] px-5 py-4">
                    <div>
                      <h2 className="text-sm font-semibold text-slate-200">
                        Watchlist
                      </h2>

                      <p className="mt-1 text-xs text-slate-600">
                        Your tracked instruments
                      </p>
                    </div>

                    <button className="text-xs text-cyan-400">
                      Manage
                    </button>
                  </div>

                  <div className="p-5">
                    {["NIFTY 50", "BANK NIFTY", "RELIANCE", "TCS"].map(
                      (symbol) => (
                        <div
                          key={symbol}
                          className="flex items-center justify-between border-b border-white/[0.05] py-3 last:border-0"
                        >
                          <div className="flex items-center gap-3">
                            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.035] text-xs text-slate-500">
                              ☆
                            </span>

                            <div>
                              <p className="text-sm font-medium text-slate-300">
                                {symbol}
                              </p>
                              <p className="text-[10px] uppercase text-slate-600">
                                NSE
                              </p>
                            </div>
                          </div>

                          <span className="font-mono text-xs text-slate-600">
                            —
                          </span>
                        </div>
                      ),
                    )}
                  </div>
                </div>
              </div>

              {/* LOWER MODULES */}
              <div className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
                {[
                  {
                    title: "Drishti AI",
                    description: "AI-powered market reasoning and insights.",
                    icon: "✦",
                  },
                  {
                    title: "Strategy",
                    description: "Build and evaluate trading strategies.",
                    icon: "◇",
                  },
                  {
                    title: "Paper Trading",
                    description: "Practice trades without real capital.",
                    icon: "◎",
                  },
                  {
                    title: "Portfolio",
                    description: "Track holdings, performance and risk.",
                    icon: "▣",
                  },
                ].map((module) => (
                  <button
                    key={module.title}
                    className="group rounded-xl border border-white/[0.07] bg-[#0d1422] p-5 text-left transition hover:-translate-y-0.5 hover:border-cyan-400/15 hover:bg-[#111a2b]"
                  >
                    <div className="mb-5 flex h-9 w-9 items-center justify-center rounded-lg bg-cyan-400/[0.07] text-cyan-300">
                      {module.icon}
                    </div>

                    <h3 className="text-sm font-semibold text-slate-200 group-hover:text-cyan-300">
                      {module.title}
                    </h3>

                    <p className="mt-2 text-xs leading-5 text-slate-600">
                      {module.description}
                    </p>
                  </button>
                ))}
              </div>

              {/* FOUNDATION NOTICE */}
              <div className="mt-5 rounded-xl border border-cyan-400/10 bg-cyan-400/[0.025] p-4">
                <div className="flex gap-3">
                  <span className="mt-0.5 text-cyan-400">✦</span>

                  <div>
                    <p className="text-xs font-medium text-cyan-300">
                      TRADEu application foundation
                    </p>

                    <p className="mt-1 text-xs leading-5 text-slate-600">
                      The main application shell is established. Market data,
                      charts, technical analysis, intelligence, trading,
                      investing and automation capabilities will be connected
                      progressively according to the TRADEu roadmap.
                    </p>
                  </div>
                </div>
              </div>

              <footer className="mt-8 border-t border-white/[0.07] pt-5 text-[11px] text-slate-700">
                TRADEu — Main Application UI — Phase 06
              </footer>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
