"use client";

import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Zap, AlertTriangle, XCircle, FileText, X } from "lucide-react";

interface Source {
  chunk_id: number;
  content: string;
  file_path: string;
  metadata: Record<string, unknown>;
}

interface AskResponse {
  answer: string;
  confidence: number;
  sources: Source[];
  chunks_used: number;
}

interface ErrorState {
  message: string;
  type: "error" | "warning";
}

export default function AskPage() {
  const [question, setQuestion] = useState("");
  const [submittedQuestion, setSubmittedQuestion] = useState("");
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ErrorState | null>(null);
  const [showSources, setShowSources] = useState(false);
  const [viewingDocument, setViewingDocument] = useState<{
    filename: string;
    content: string;
  } | null>(null);
  const [loadingDoc, setLoadingDoc] = useState(false);
  const answerRef = useRef<HTMLDivElement>(null);

  // Quick suggestions
  const suggestions = [
    "How do I set up my development environment?",
    "What is the CI/CD pipeline?",
    "How do I run tests?",
    "What are the security best practices?",
  ];

  const viewFullDocument = async (filename: string) => {
    setLoadingDoc(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/docs/${filename}`);

      if (!res.ok) {
        throw new Error(`Failed to load document: ${res.statusText}`);
      }

      const data = await res.json();
      setViewingDocument({ filename: data.filename, content: data.content });
    } catch (err) {
      console.error("Error loading document:", err);
      setError({
        message: err instanceof Error ? err.message : "Failed to load document",
        type: "error",
      });
    } finally {
      setLoadingDoc(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!question.trim()) {
      setError({ message: "Please enter a question", type: "warning" });
      return;
    }

    if (question.length > 500) {
      setError({
        message: "Question must be 500 characters or less",
        type: "warning",
      });
      return;
    }

    // Reset states
    setError(null);
    setResponse(null);
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (!res.ok) {
        const errorData = await res
          .json()
          .catch(() => ({ detail: "Unknown error" }));
        throw new Error(
          errorData.detail || `HTTP ${res.status}: ${res.statusText}`,
        );
      }

      const data: AskResponse = await res.json();
      setResponse(data);
      setSubmittedQuestion(question.trim());
      setQuestion("");

      // Auto-expand sources if confidence is low
      if (data.confidence < 0.7) {
        setShowSources(true);
      }
    } catch (err) {
      console.error("Error asking question:", err);
      setError({
        message:
          err instanceof Error
            ? err.message
            : "Failed to get answer. Please check if the backend is running.",
        type: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuestion(suggestion);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.7) return "text-green-600 dark:text-green-400";
    if (confidence >= 0.5) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getConfidenceBg = (confidence: number) => {
    if (confidence >= 0.7) return "bg-green-100 dark:bg-green-900/30";
    if (confidence >= 0.5) return "bg-yellow-100 dark:bg-yellow-900/30";
    return "bg-red-100 dark:bg-red-900/30";
  };

  return (
    <div className="min-h-screen bg-[var(--background)] grid-pattern">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        {/* Chat Container */}
        <div className="space-y-8">
          {/* Initial State */}
          {!response && !loading && !error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center space-y-12"
            >
              <div>
                <h1 className="text-4xl sm:text-5xl font-bold text-[var(--foreground)] mb-4">
                  What would you like to know?
                </h1>
                <p className="text-[var(--muted)] text-lg">
                  Ask about processes, tools, or engineering practices
                </p>
              </div>

              {/* Quick Suggestions */}
              <div className="flex flex-wrap gap-3 justify-center">
                {suggestions.map((suggestion, idx) => (
                  <motion.button
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * idx }}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="text-sm px-4 py-2 border border-[var(--border)] text-[var(--muted)] hover:border-[var(--accent)] hover:text-[var(--accent)] transition-all rounded-none"
                  >
                    {suggestion}
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Question Display (After submission) */}
          <AnimatePresence>
            {submittedQuestion && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="flex justify-end"
              >
                <div className="max-w-[80%]">
                  <div className="text-xs font-mono font-semibold tracking-tight text-[var(--subtle)] mb-2 text-right uppercase">
                    YOU
                  </div>
                  <div className="bg-black dark:bg-white text-white dark:text-black px-6 py-4 text-lg">
                    {submittedQuestion}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Loading State */}
          {loading && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex justify-start"
            >
              <div className="max-w-[80%]">
                <div className="text-xs font-mono font-semibold tracking-tight text-[var(--subtle)] mb-2 uppercase">
                  COPILOT
                </div>
                <div className="bg-[var(--surface)] border-2 border-[var(--border)] px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-[var(--foreground)] rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-[var(--foreground)] rounded-full animate-pulse [animation-delay:0.2s]"></div>
                      <div className="w-2 h-2 bg-[var(--foreground)] rounded-full animate-pulse [animation-delay:0.4s]"></div>
                    </div>
                    <span className="text-[var(--muted)]">Thinking...</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Error State */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className={`border-2 px-6 py-4 ${
                  error.type === "error"
                    ? "border-red-500 bg-red-50 dark:bg-red-900/20"
                    : "border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20"
                }`}
              >
                <div className="flex items-start gap-3">
                  {error.type === "error" ? (
                    <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                  ) : (
                    <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" />
                  )}
                  <div>
                    <h3
                      className={`font-bold mb-1 ${
                        error.type === "error"
                          ? "text-red-800 dark:text-red-400"
                          : "text-yellow-800 dark:text-yellow-400"
                      }`}
                    >
                      {error.type === "error" ? "Error" : "Warning"}
                    </h3>
                    <p
                      className={
                        error.type === "error"
                          ? "text-red-700 dark:text-red-300"
                          : "text-yellow-700 dark:text-yellow-300"
                      }
                    >
                      {error.message}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Answer Display */}
          <AnimatePresence>
            {response && !loading && (
              <motion.div
                ref={answerRef}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4 }}
                className="flex justify-start"
              >
                <div className="max-w-[85%] w-full">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-xs font-mono font-semibold tracking-tight text-[var(--subtle)] uppercase">
                      COPILOT
                    </div>
                    {response.sources.length > 0 && (
                      <div
                        className={`flex items-center gap-2 px-3 py-1 ${getConfidenceBg(response.confidence)} ${getConfidenceColor(response.confidence)} text-sm font-mono font-bold`}
                      >
                        {response.confidence >= 0.7 ? (
                          <Zap className="w-4 h-4" />
                        ) : response.confidence >= 0.5 ? (
                          <AlertTriangle className="w-4 h-4" />
                        ) : (
                          <XCircle className="w-4 h-4" />
                        )}
                        {(response.confidence * 100).toFixed(0)}%
                      </div>
                    )}
                  </div>
                  <div className="bg-[var(--surface)] border-2 border-[var(--border)] px-6 py-6">
                    <p className="text-[var(--foreground)] text-lg leading-relaxed whitespace-pre-wrap">
                      {response.answer}
                    </p>

                    {/* Sources */}
                    {response.sources.length > 0 && (
                      <div className="mt-6 pt-6 border-t border-[var(--border)]">
                        <button
                          onClick={() => setShowSources(!showSources)}
                          className="flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
                        >
                          <FileText className="w-4 h-4" />
                          <span>
                            Sources: {new Set(response.sources.map((s) => s.file_path.split("/").pop())).size} file
                            {new Set(response.sources.map((s) => s.file_path)).size !== 1 ? "s" : ""}
                          </span>
                          <span className="text-xs">{showSources ? "▼" : "▶"}</span>
                        </button>

                        <AnimatePresence>
                          {showSources && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="mt-4 space-y-2 overflow-hidden"
                            >
                              {Array.from(
                                new Set(response.sources.map((s) => s.file_path))
                              ).map((filePath) => {
                                const filename = filePath.split("/").pop() || filePath;
                                return (
                                  <button
                                    key={filePath}
                                    onClick={() => viewFullDocument(filename)}
                                    className="w-full px-4 py-3 bg-[var(--background)] border border-[var(--border)] hover:border-[var(--accent)] transition-all text-left group"
                                  >
                                    <div className="flex items-center gap-2">
                                      <FileText className="w-4 h-4 text-[var(--accent)] group-hover:scale-110 transition-transform" />
                                      <span className="text-sm font-medium text-[var(--foreground)] group-hover:text-[var(--accent)]">
                                        {filename}
                                      </span>
                                    </div>
                                  </button>
                                );
                              })}
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Input Form (Always at bottom) */}
        <div className="fixed bottom-0 left-0 right-0 border-t-2 border-[var(--border)] bg-[var(--surface)]">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 py-4">
            <form onSubmit={handleSubmit} className="flex gap-3">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask another question..."
                  className="w-full px-6 py-3 bg-[var(--background)] border-2 border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--subtle)] focus:border-[var(--foreground)] focus:outline-none transition-colors text-base font-normal"
                  disabled={loading}
                  maxLength={500}
                />
                <span className="absolute right-6 top-1/2 -translate-y-1/2 text-xs font-mono text-[var(--subtle)]">
                  {question.length}/500
                </span>
              </div>
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className="px-6 py-3 bg-black dark:bg-white text-white dark:text-black font-semibold hover:scale-[1.02] disabled:opacity-20 disabled:hover:scale-100 transition-all flex items-center justify-center"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>

        {/* Spacer for fixed input */}
        <div className="h-24"></div>
      </div>

      {/* Document Viewer Modal */}
      <AnimatePresence>
        {viewingDocument && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={() => setViewingDocument(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-[var(--surface)] border-2 border-[var(--border)] w-full max-w-4xl max-h-[90vh] flex flex-col"
            >
              {/* Modal Header */}
              <div className="flex items-center justify-between p-6 border-b border-[var(--border)]">
                <div className="flex items-center gap-3">
                  <FileText className="w-6 h-6 text-[var(--accent)]" />
                  <div>
                    <h2 className="text-xl font-bold text-[var(--foreground)]">
                      {viewingDocument.filename}
                    </h2>
                    <p className="text-sm text-[var(--muted)]">
                      Full documentation
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setViewingDocument(null)}
                  className="text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Modal Content */}
              <div className="flex-1 overflow-y-auto p-6">
                <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-[var(--foreground)]">
                  {viewingDocument.content}
                </pre>
              </div>

              {/* Modal Footer */}
              <div className="flex items-center justify-end p-6 border-t border-[var(--border)]">
                <button
                  onClick={() => setViewingDocument(null)}
                  className="px-6 py-3 bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)] font-medium hover:border-[var(--accent)] transition-colors"
                >
                  Close
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading Document Overlay */}
      <AnimatePresence>
        {loadingDoc && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50"
          >
            <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-6 flex items-center gap-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-[var(--foreground)] rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-[var(--foreground)] rounded-full animate-pulse [animation-delay:0.2s]"></div>
                <div className="w-2 h-2 bg-[var(--foreground)] rounded-full animate-pulse [animation-delay:0.4s]"></div>
              </div>
              <span className="text-[var(--foreground)] font-medium">
                Loading document...
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
