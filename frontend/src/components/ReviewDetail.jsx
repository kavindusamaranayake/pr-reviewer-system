import React, { useState } from "react";
import { reviewsAPI } from "../services/api";

function ReviewDetail({ review, onClose }) {
  const [decision, setDecision] = useState("");
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (action) => {
    setSubmitting(true);
    setError(null);

    try {
      await reviewsAPI.makeDecision(review.id, action, notes || null);
      onClose();
    } catch (err) {
      setError(`Failed to ${action} review`);
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case "error":
        return (
          <svg
            className="h-5 w-5 text-red-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        );
      case "warning":
        return (
          <svg
            className="h-5 w-5 text-yellow-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
        );
      default:
        return (
          <svg
            className="h-5 w-5 text-blue-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
              clipRule="evenodd"
            />
          </svg>
        );
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
        {/* Header */}
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              {review.pr_title}
            </h3>
            <p className="text-sm text-gray-500">
              PR #{review.pr_number} by {review.pr_author} •{" "}
              {review.branch_type}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* PR Info */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Branch:</span>
              <span className="ml-2 text-gray-900">{review.branch_name}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Status:</span>
              <span
                className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
                  review.status === "pending"
                    ? "bg-yellow-100 text-yellow-800"
                    : review.status === "posted"
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"
                }`}
              >
                {review.status}
              </span>
            </div>
            <div className="col-span-2">
              <a
                href={review.pr_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-indigo-600 hover:text-indigo-800 flex items-center"
              >
                View on GitHub
                <svg
                  className="h-4 w-4 ml-1"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                  />
                </svg>
              </a>
            </div>
          </div>
        </div>

        {/* Review Summary */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-3">
            Review Summary
          </h4>
          <div className="bg-gray-50 rounded-lg p-4 prose prose-sm max-w-none">
            <pre className="whitespace-pre-wrap font-sans text-sm text-gray-700">
              {review.review_summary}
            </pre>
          </div>
        </div>

        {/* Feedback Items */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-3">
            Detailed Feedback
          </h4>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {review.review_feedback.map((item, index) => (
              <div
                key={index}
                className="flex items-start p-3 bg-white border border-gray-200 rounded-lg"
              >
                <div className="flex-shrink-0 mr-3">
                  {getSeverityIcon(item.severity)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-gray-900">
                      {item.category}
                    </span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded ${
                        item.severity === "error"
                          ? "bg-red-100 text-red-800"
                          : item.severity === "warning"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-blue-100 text-blue-800"
                      }`}
                    >
                      {item.severity}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">{item.message}</p>
                  {item.file_path && (
                    <p className="text-xs text-gray-500 mt-1">
                      File: {item.file_path}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Branch Expectations */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-3">
            Branch Requirements
          </h4>
          <div className="bg-indigo-50 rounded-lg p-4">
            <p className="text-sm text-gray-700 mb-2">
              {review.expectations_applied.description}
            </p>
            <ul className="text-sm text-gray-600 space-y-1">
              {review.expectations_applied.checks?.map((check, index) => (
                <li key={index} className="flex items-start">
                  <svg
                    className="h-4 w-4 text-indigo-600 mr-2 mt-0.5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clipRule="evenodd"
                    />
                  </svg>
                  {check}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Instructor Actions (only for pending reviews) */}
        {review.status === "pending" && (
          <div className="border-t pt-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">
              Instructor Decision
            </h4>

            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Additional Notes (Optional)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Add any additional comments for the student..."
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => handleSubmit("approve")}
                disabled={submitting}
                className="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {submitting ? "Processing..." : "✓ Approve & Post to GitHub"}
              </button>
              <button
                onClick={() => handleSubmit("reject")}
                disabled={submitting}
                className="flex-1 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {submitting ? "Processing..." : "✗ Reject Review"}
              </button>
            </div>
          </div>
        )}

        {/* Show instructor notes if review was already processed */}
        {review.status !== "pending" && review.instructor_notes && (
          <div className="border-t pt-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">
              Instructor Notes
            </h4>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-700">{review.instructor_notes}</p>
            </div>
          </div>
        )}
      </div>
      //{" "}
    </div>
  );
}

export default ReviewDetail;
