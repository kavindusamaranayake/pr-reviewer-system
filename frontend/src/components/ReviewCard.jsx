import React from "react";

function ReviewCard({ review, onClick }) {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case "error":
        return "text-red-600";
      case "warning":
        return "text-yellow-600";
      case "info":
        return "text-blue-600";
      default:
        return "text-gray-600";
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      pending: "bg-yellow-100 text-yellow-800",
      posted: "bg-green-100 text-green-800",
      rejected: "bg-red-100 text-red-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const errorCount = review.review_feedback.filter(
    (f) => f.severity === "error"
  ).length;
  const warningCount = review.review_feedback.filter(
    (f) => f.severity === "warning"
  ).length;

  return (
    <div
      onClick={onClick}
      className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(
                review.status
              )}`}
            >
              {review.status}
            </span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              {review.branch_type}
            </span>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-1 line-clamp-2">
            {review.pr_title}
          </h3>
          <p className="text-sm text-gray-500 mb-3">
            #{review.pr_number} by {review.pr_author}
          </p>
        </div>
      </div>

      <div className="mt-4 flex items-center gap-4 text-sm">
        {errorCount > 0 && (
          <div className="flex items-center text-red-600">
            <svg
              className="h-5 w-5 mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            {errorCount} errors
          </div>
        )}
        {warningCount > 0 && (
          <div className="flex items-center text-yellow-600">
            <svg
              className="h-5 w-5 mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
            {warningCount} warnings
          </div>
        )}
      </div>

      <div className="mt-4 text-xs text-gray-500">
        {new Date(review.created_at).toLocaleString()}
      </div>
    </div>
  );
}

export default ReviewCard;
