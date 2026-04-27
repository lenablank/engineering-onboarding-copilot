"use client";

import { motion } from "framer-motion";
import { ArrowRight, BookOpen, Radar, Sparkles } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[var(--background)] grid-pattern flex items-center justify-center p-4 sm:p-8">
      <div className="max-w-5xl w-full text-center">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="mb-16 sm:mb-24 pt-16 sm:pt-24"
        >
          <h1 className="text-6xl sm:text-7xl lg:text-8xl font-mono font-bold text-[var(--foreground)] mb-6 tracking-tight leading-[0.9]">
            ENGINEERING
            <br />
            ONBOARDING
            <br />
            COPILOT
          </h1>
          <p className="text-lg sm:text-xl text-[var(--muted)] max-w-2xl mx-auto font-light">
            Your AI documentation companion
          </p>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
          className="flex flex-col sm:flex-row gap-4 justify-center mb-16 sm:mb-24"
        >
          <Link
            href="/ask"
            className="group inline-flex items-center justify-center gap-3 px-8 py-5 text-lg font-mono font-semibold text-white bg-black dark:bg-white dark:text-black rounded-none hover:scale-[1.02] transition-all shadow-[4px_4px_0_0_rgba(0,0,0,1)] dark:shadow-[4px_4px_0_0_rgba(255,255,255,1)] hover:shadow-[6px_6px_0_0_rgba(0,0,0,1)] dark:hover:shadow-[6px_6px_0_0_rgba(255,255,255,1)] w-full sm:w-64"
          >
            Ask a Question
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            href="/gaps"
            className="group inline-flex items-center justify-center gap-3 px-8 py-5 text-lg font-mono font-semibold text-black dark:text-white bg-white dark:bg-black border-2 border-black dark:border-white rounded-none hover:scale-[1.02] transition-all shadow-[4px_4px_0_0_rgba(0,0,0,1)] dark:shadow-[4px_4px_0_0_rgba(255,255,255,1)] hover:shadow-[6px_6px_0_0_rgba(0,0,0,1)] dark:hover:shadow-[6px_6px_0_0_rgba(255,255,255,1)] w-full sm:w-64"
          >
            View Gaps
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="grid md:grid-cols-3 gap-6 sm:gap-8 mb-16 sm:mb-24"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.5 }}
            className="group bg-[var(--surface)] border-2 border-[var(--border)] p-8 hover:border-[var(--accent)] transition-all text-center"
          >
            <div className="flex items-center justify-center gap-3 mb-3">
              <Sparkles className="w-5 h-5 text-[var(--foreground)]" />
              <h3 className="text-lg font-mono font-bold text-[var(--foreground)]">
                AI-Powered Answers
              </h3>
            </div>
            <p className="text-[var(--muted)] leading-relaxed">
              Instant responses using Groq LLM and semantic search
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.6 }}
            className="group bg-[var(--surface)] border-2 border-[var(--border)] p-8 hover:border-[var(--accent)] transition-all text-center"
          >
            <div className="flex items-center justify-center gap-3 mb-3">
              <BookOpen className="w-5 h-5 text-[var(--foreground)]" />
              <h3 className="text-lg font-mono font-bold text-[var(--foreground)]">
                Source Citations
              </h3>
            </div>
            <p className="text-[var(--muted)] leading-relaxed">
              Every answer includes verifiable documentation sources
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.7 }}
            className="group bg-[var(--surface)] border-2 border-[var(--border)] p-8 hover:border-[var(--accent)] transition-all text-center"
          >
            <div className="flex items-center justify-center gap-3 mb-3">
              <Radar className="w-5 h-5 text-[var(--foreground)]" />
              <h3 className="text-lg font-mono font-bold text-[var(--foreground)]">
                Gap Radar
              </h3>
            </div>
            <p className="text-[var(--muted)] leading-relaxed">
              Automatically tracks documentation gaps
            </p>
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="text-center"
        >
          <p className="text-sm text-[var(--subtle)] font-mono">
            Powered by Groq • ChromaDB • Cohere
          </p>
        </motion.div>
      </div>
    </div>
  );
}
