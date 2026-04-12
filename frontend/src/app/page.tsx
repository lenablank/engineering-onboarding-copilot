import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-8">
      <div className="max-w-3xl text-center">
        {/* Logo/Title */}
        <div className="mb-8">
          <h1 className="text-5xl sm:text-6xl font-bold text-slate-900 dark:text-white mb-4">
            Engineering Onboarding Copilot
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            Your AI-powered guide to engineering processes, tools, and best
            practices
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-lg">
            <div className="text-4xl mb-3">🤖</div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
              AI-Powered Answers
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Get instant answers using Groq LLM and semantic search
            </p>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-lg">
            <div className="text-4xl mb-3">📚</div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
              Source Citations
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Every answer includes source documentation for verification
            </p>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-lg">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
              Gap Radar
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Automatically tracks documentation gaps to improve knowledge base
            </p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/ask"
            className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
          >
            Start Asking Questions
            <span>→</span>
          </Link>
          <Link
            href="/gaps"
            className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-blue-600 bg-white border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition-colors shadow-lg hover:shadow-xl"
          >
            View Gap Radar
            <span>→</span>
          </Link>
        </div>

        {/* Tech Stack */}
        <div className="mt-12 pt-8 border-t border-slate-200 dark:border-slate-700">
          <p className="text-sm text-slate-500 dark:text-slate-400 mb-3">
            Built with
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-600 dark:text-slate-400">
            <span className="px-3 py-1 bg-slate-200 dark:bg-slate-700 rounded-full">
              Next.js 14
            </span>
            <span className="px-3 py-1 bg-slate-200 dark:bg-slate-700 rounded-full">
              FastAPI
            </span>
            <span className="px-3 py-1 bg-slate-200 dark:bg-slate-700 rounded-full">
              LangChain
            </span>
            <span className="px-3 py-1 bg-slate-200 dark:bg-slate-700 rounded-full">
              ChromaDB
            </span>
            <span className="px-3 py-1 bg-slate-200 dark:bg-slate-700 rounded-full">
              Groq (Llama 3.1)
            </span>
            <span className="px-3 py-1 bg-slate-200 dark:bg-slate-700 rounded-full">
              HuggingFace
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
