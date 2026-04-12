"use client";

import { useEffect, useState } from "react";

// Types matching backend API
interface Gap {
  id: string;
  question: string;
  confidence_score: number;
  frequency: number;
  status: "NEW" | "REVIEWED" | "RESOLVED";
  retrieval_context: Array<Record<string, any>>;
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
    let aVal: any = a[sortField];
    let bVal: any = b[sortField];

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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Documentation Gap Radar
          </h1>
          <p className="text-gray-600">
            Track questions where documentation coverage is insufficient
          </p>
        </div>

        {/* Statistics Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-1">Total Gaps</div>
              <div className="text-3xl font-bold text-gray-900">
                {stats.total_gaps}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-1">
                Total Occurrences
              </div>
              <div className="text-3xl font-bold text-gray-900">
                {stats.total_occurrences}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-1">New</div>
              <div className="text-3xl font-bold text-red-600">
                {stats.by_status.NEW || stats.by_status.new || 0}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-1">Reviewed</div>
              <div className="text-3xl font-bold text-yellow-600">
                {stats.by_status.REVIEWED || stats.by_status.reviewed || 0}
              </div>
            </div>
          </div>
        )}

        {/* Filters and Controls */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium text-gray-700">
                Status:
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All</option>
                <option value="NEW">New</option>
                <option value="REVIEWED">Reviewed</option>
                <option value="RESOLVED">Resolved</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <label className="text-sm font-medium text-gray-700">
                Sort by:
              </label>
              <select
                value={sortField}
                onChange={(e) => setSortField(e.target.value as SortField)}
                className="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="frequency">Frequency</option>
                <option value="created_at">Date</option>
                <option value="confidence_score">Confidence</option>
              </select>
            </div>

            <button
              onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
              className="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
            >
              {sortOrder === "asc" ? "↑ Ascending" : "↓ Descending"}
            </button>

            <button
              onClick={fetchData}
              className="ml-auto px-4 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Refresh
            </button>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent mb-4"></div>
            <p className="text-gray-600">Loading gaps...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && sortedGaps.length === 0 && (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No documentation gaps found!
            </h3>
            <p className="text-gray-600">
              {statusFilter !== "all"
                ? `No gaps with status "${statusFilter}"`
                : "All questions are well-documented."}
            </p>
          </div>
        )}

        {/* Gaps Table */}
        {!loading && !error && sortedGaps.length > 0 && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Question
                    </th>
                    <th
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                      onClick={() => handleSort("frequency")}
                    >
                      Frequency{" "}
                      {sortField === "frequency" &&
                        (sortOrder === "asc" ? "↑" : "↓")}
                    </th>
                    <th
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                      onClick={() => handleSort("confidence_score")}
                    >
                      Confidence{" "}
                      {sortField === "confidence_score" &&
                        (sortOrder === "asc" ? "↑" : "↓")}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                      onClick={() => handleSort("created_at")}
                    >
                      First Seen{" "}
                      {sortField === "created_at" &&
                        (sortOrder === "asc" ? "↑" : "↓")}
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {sortedGaps.map((gap) => (
                    <tr key={gap.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900 max-w-md">
                          {gap.question}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {gap.frequency}x
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {(gap.confidence_score * 100).toFixed(1)}%
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(gap.status)}`}
                        >
                          {gap.status.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
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
          <div className="mt-4 text-sm text-gray-600 text-center">
            Showing {sortedGaps.length} gap{sortedGaps.length !== 1 ? "s" : ""}
            {statusFilter !== "all" && ` with status "${statusFilter}"`}
          </div>
        )}
      </div>
    </div>
  );
}
