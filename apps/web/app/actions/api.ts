"use server";

import { EvaluateRequest } from "@/lib/api";

export async function sendEvaluateRequest(request: EvaluateRequest) {
  return fetch("http://localhost:5001/api/v1/evaluate/stream", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
