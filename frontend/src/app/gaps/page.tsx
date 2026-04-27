"use client";

import { useEffect, useState } from "react";

// Types matching backend API
interface Gap {
  id: string;
  question: string;
  confidence_score: number;
  frequency: number;
  status: "NEW" | "REVIEWED" | "RESOLVED";
  retrieval_context: Array<Record<string, unknown>>;
  created_at: string;
  updated_at: string;
}

interface GapStats {
  total_gaps: number;
  total_occurrences: number;
  by_status: Record<string, number>;
  most_frequent: Gap | null;
}

type SortField = "frequency" | "created_at" | "confidence_score";
type SortOrder = "asc" | "desc";

export default function GapsPage() {
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [stats, setStats] = useState<GapStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters and sorting
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [sortField, setSortField] = useState<SortField>("frequency");
  const [sortOrder, setSortOrder] = useState<SortOrder>("desc");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  // Fetch gaps and statistics
  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch gaps (note trailing slash required by FastAPI)
      const statusParam =
        statusFilter !== "all" ? `?status=${statusFilter}` : "";
      const gapsRes = await fetch(`${apiUrl}/api/gaps/${statusParam}`);

      if (!gapsRes.ok) {
        throw new Error(`Failed to load gaps: ${gapsRes.statusText}`);
      }

      const gapsData = await gapsRes.json();

      // Fetch statistics
      const statsRes = await fetch(`${apiUrl}/api/gaps/stats`);
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }

      setGaps(gapsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
      console.error("Error fetching gaps:", err);
    } finally {
      setLoading(false);
    }
  };

  // Client-side sorting
  const sortedGaps = [...gaps].sort((a, b) => {
    let aVal: number | string = a[sortField];
    let bVal: number | string = b[sortField];

    // Handle date fields
    if (sortField === "created_at") {
      aVal = new Date(aVal).getTime();
      bVal = new Date(bVal).getTime();
    }

    if (sortOrder === "asc") {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  // Status color coding (handle both upper and lowercase)
  const getStatusColor = (status: string) => {
    const normalizedStatus = status.toUpperCase();
    switch (normalizedStatus) {
      case "NEW":
        return "bg-red-100 text-red-800";
      case "REVIEWED":
        return "bg-yellow-100 text-yellow-800";
      case "RESOLVED":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  // Toggle sort
  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("desc");
    }
  };

  return (
    <div className="min-h-screen bg-[var(--background)] grid-pattern p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl sm:text-5xl font-mono font-bold text-[var(--foreground)] mb-3 tracking-tight">
            DOCUMENTATION GAP RADAR
          </h1>
          <p className="text-lg text-[var(--muted)]">
            Track questions where documentation coverage is insufficient
          </p>
        </div>

        {/* Statistics Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-6">
              <div className="text-xs font-mono font-semibold text-[var(--subtle)] mb-2 uppercase tracking-tight">Total Gaps</div>
              <div className="text-3xl font-mono font-bold text-[var(--foreground)]">
                {stats.total_gaps}
              </div>
            </div>

            <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-6">
              <div className="text-xs font-mono font-semibold text-[var(--subtle)] mb-2 uppercase tracking-tight">
                Total Occurrences
              </div>
              <div className="text-3xl font-mono font-bold text-[var(--foreground)]">
                {stats.total_occurrences}
              </div>
            </div>

            <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-6">
              <div className="text-xs font-mono font-semibold text-[var(--subtle)] mb-2 uppercase tracking-tight">New</div>
              <div className="text-3xl font-mono font-bold text-red-600">
                {stats.by_status.NEW || stats.by_status.new || 0}
              </div>
            </div>

            <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-6">
              <div className="text-xs font-mono font-semibold text-[var(--subtle)] mb-2 uppercase tracking-tight">Reviewed</div>
              <div className="text-3xl font-mono font-bold text-yellow-600">
                {stats.by_status.REVIEWED || stats.by_status.reviewed || 0}
              </div>
            </div>
          </div>
        )}

        {/* Filters and Controls */}
        <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-4 mb-8">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-2">
              <label className="text-sm font-mono font-semibold text-[var(--foreground)]">
                Status:
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="border-2 border-[var(--border)] bg-[var(--background)] rounded-none px-3 py-1.5 text-sm font-mono focus:outline-none focus:border-[var(--accent)]"
              >
                <option value="all">All</option>
                <option value="NEW">New</option>
                <option value="REVIEWED">Reviewed</option>
                <option value="RESOLVED">Resolved</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <label className="text-sm font-mono font-semibold text-[var(--foreground)]">
                Sort by:
              </label>
              <select
                value={sortField}
                onChange={(e) => setSortField(e.target.value as SortField)}
                className="border-2 border-[var(--border)] bg-[var(--background)] rounded-none px-3 py-1.5 text-sm font-mono focus:outline-none focus:border-[var(--accent)]"
              >
                <option value="frequency">Frequency</option>
                <option value="created_at">Date</option>
                <option value="confidence_score">Confidence</option>
              </select>
            </div>

            <button
              onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
              className="px-3 py-1.5 text-sm font-mono font-semibold border-2 border-[var(--border)] rounded-none hover:border-[var(--accent)] transition-colors"
            >
              {sortOrder === "asc" ? "↑ Ascending" : "↓ Descending"}
            </button>

            <button
              onClick={fetchData}
              className="ml-auto px-4 py-1.5 text-sm font-mono font-semibold bg-[var(--foreground)] text-[var(--background)] rounded-none hover:bg-[var(--accent)] transition-colors"
            >
              Refresh
            </button>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-12 text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[var(--foreground)] border-r-transparent mb-4"></div>
            <p className="text-[var(--muted)] font-mono">Loading gaps...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-2 border-red-600 rounded-none p-4 mb-6">
            <p className="text-red-800 font-mono">{error}</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && sortedGaps.length === 0 && (
          <div className="bg-[var(--surface)] border-2 border-[var(--border)] p-12 text-center">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-xl font-mono font-bold text-[var(--foreground)] mb-2">
              No documentation gaps found!
            </h3>
            <p className="text-[var(--muted)]">
              {statusFilter !== "all"
                ? `No gaps with status "${statusFilter}"`
                : "All questions are well-documented."}
            </p>
          </div>
        )}

        {/* Gaps Table */}
        {!loading && !error && sortedGaps.length > 0 && (
          <div className="bg-[var(--surface)] border-2 border-[var(--border)] overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y-2 divide-[var(--border)]">
                <thead className="bg-[var(--background)]">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-mono font-bold text-[var(--foreground)] uppercase tracking-tight">
                      Question
                    </th>
                    <th
                      className="px-6 py-3 text-left text-xs font-mono font-bold text-[var(--foreground)] uppercase tracking-tight cursor-pointer hover:text-[var(--accent)]"
                      onClick={() => handleSort("frequency")}
                    >
                      Frequency{" "}
                      {sortField === "frequency" &&
                        (sortOrder === "asc" ? "↑" : "↓")}
                    </th>
                    <th
                      className="px-6 py-3 text-left text-xs font-mono font-bold text-[var(--foreground)] uppercase tracking-tight cursor-pointer hover:text-[var(--accent)]"
                      onClick={() => handleSort("confidence_score")}
                    >
                      Confidence{" "}
                      {sortField === "confidence_score" &&
                        (sortOrder === "asc" ? "↑" : "↓")}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-mono font-bold text-[var(--foreground)] uppercase tracking-tight">
                      Status
                    </th>
                    <th
                      className="px-6 py-3 text-left text-xs font-mono font-bold text-[var(--foreground)] uppercase tracking-tight cursor-pointer hover:text-[var(--accent)]"
                      onClick={() => handleSort("created_at")}
                    >
                      First Seen{" "}
                      {sortField === "created_at" &&
                        (sortOrder === "asc" ? "↑" : "↓")}
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-[var(--surface)] divide-y-2 divide-[var(--border)]">
                  {sortedGaps.map((gap) => (
                    <tr key={gap.id} className="hover:bg-[var(--background)] transition-colors">
                      <td className="px-6 py-4">
                        <div className="text-sm text-[var(--foreground)] max-w-md">
                          {gap.question}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-none text-xs font-mono font-bold bg-blue-100 text-blue-800 border border-blue-800">
                          {gap.frequency}x
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-mono font-bold text-[var(--foreground)]">
                          {(gap.confidence_score * 100).toFixed(1)}%
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-none text-xs font-mono font-bold ${getStatusColor(gap.status)}`}
                        >
                          {gap.status.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-[var(--muted)]">
                        {formatDate(gap.created_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Footer Info */}
        {!loading && !error && sortedGaps.length > 0 && (
          <div className="mt-6 text-sm font-mono text-[var(--subtle)] text-center">
            Showing {sortedGaps.length} gap{sortedGaps.length !== 1 ? "s" : ""}
            {statusFilter !== "all" && ` with status "${statusFilter}"`}
          </div>
        )}
      </div>
    </div>
  );
}
