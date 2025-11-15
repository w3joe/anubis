"use server";

import { EvaluateRequest } from "@/lib/api";

// Note: This function is kept for backwards compatibility but is not recommended for streaming.
// Use the /api/evaluate/stream route handler directly from the client for proper streaming.
export async function sendEvaluateRequest(request: EvaluateRequest) {
  try {
    const response = await fetch(
      "http://localhost:5001/api/v1/evaluate/stream",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      }
    );

    // Return a serializable object instead of the Response object
    return {
      ok: response.ok,
      status: response.status,
      statusText: response.statusText,
      data: response.ok ? await response.json() : null,
    };
  } catch (error) {
    return {
      ok: false,
      status: 500,
      statusText: error instanceof Error ? error.message : "Unknown error",
      data: null,
    };
  }
}
