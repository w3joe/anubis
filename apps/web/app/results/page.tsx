"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import {
  Model,
  Metric,
  ModelResult,
  Recommendation,
  Warning,
  StreamEvent,
  EvaluationMetrics,
} from "@/lib/types";
import { ModelOutputCard } from "@/components/model-output-card";
import { RecommendationSection } from "@/components/recommendation-section";
import { WarningsSection } from "@/components/warnings-section";
import { Button } from "@/components/ui/button";
import Link from "next/link";

// Helper function to generate pros and cons from metrics
function generateProsAndCons(metrics: EvaluationMetrics): {
  pros: string[];
  cons: string[];
} {
  const pros: string[] = [];
  const cons: string[] = [];

  Object.entries(metrics).forEach(([key, value]) => {
    const metricName = key.replace(/_/g, " ");
    const score = value.score;
    const notes = value.notes;

    if (score >= 8) {
      pros.push(`Excellent ${metricName} (${score}/10): ${notes}`);
    } else if (score >= 6.5) {
      pros.push(`Good ${metricName} (${score}/10): ${notes}`);
    } else if (score >= 5) {
      cons.push(`Moderate ${metricName} (${score}/10): ${notes}`);
    } else {
      cons.push(`Poor ${metricName} (${score}/10): ${notes}`);
    }
  });

  return { pros, cons };
}

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const router = useRouter();

  // Get parameters from URL
  const prompt = searchParams.get("prompt") || "";
  const modelsParam = searchParams.get("models") || "";
  const metricsParam = searchParams.get("metrics") || "";

  const models: Model[] = modelsParam
    ? (modelsParam.split(",") as Model[])
    : [];
  const metrics: Metric[] = metricsParam
    ? (metricsParam.split(",") as Metric[])
    : [];

  // State management
  const [results, setResults] = useState<Partial<Record<Model, ModelResult>>>(
    {}
  );
  const [recommendation, setRecommendation] = useState<Recommendation | null>(
    null
  );
  const [warnings, setWarnings] = useState<Warning[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Initialize results for all models
    const initialResults: Partial<Record<Model, ModelResult>> = {};
    models.forEach((model) => {
      initialResults[model] = {
        model,
        status: "pending",
        code: "",
      };
    });
    setResults(initialResults);

    // Start streaming
    startEvaluation();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const startEvaluation = async () => {
    try {
      const response = await fetch("/api/evaluate/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt,
          models,
          metrics,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No response body");
      }

      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          setIsComplete(true);
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            try {
              const event = JSON.parse(data) as StreamEvent;
              handleStreamEvent(event);
            } catch (e) {
              console.error("Failed to parse event:", e);
            }
          }
        }
      }
    } catch (err) {
      console.error("Error during evaluation:", err);
      setError(
        err instanceof Error ? err.message : "An unknown error occurred"
      );
    }
  };

  const handleStreamEvent = (event: StreamEvent) => {
    switch (event.type) {
      case "generation_start":
        setResults((prev) => {
          const currentResult = prev[event.model];
          if (!currentResult) return prev;
          return {
            ...prev,
            [event.model]: {
              ...currentResult,
              status: "processing",
            },
          };
        });
        break;

      case "code_chunk":
        setResults((prev) => {
          const currentResult = prev[event.model];
          if (!currentResult) return prev;
          return {
            ...prev,
            [event.model]: {
              ...currentResult,
              code: currentResult.code + event.chunk,
            },
          };
        });
        break;

      case "generation_complete":
        setResults((prev) => {
          const currentResult = prev[event.model];
          if (!currentResult) return prev;
          return {
            ...prev,
            [event.model]: {
              ...currentResult,
              status: event.success ? "complete" : "error",
              executionTime: event.execution_time_ms,
              error: event.success ? undefined : "Generation failed",
            },
          };
        });
        break;

      case "evaluation_result":
        setResults((prev) => {
          const currentResult = prev[event.model];
          if (!currentResult) return prev;

          // Generate pros and cons from metrics
          const { pros, cons } = generateProsAndCons(event.metrics);

          return {
            ...prev,
            [event.model]: {
              ...currentResult,
              overallScore: event.overall_score,
              metrics: event.metrics,
              pros,
              cons,
            },
          };
        });
        break;

      case "summary":
        const bestModel = event.data.best_model;
        setRecommendation({
          bestModel: bestModel,
          bestScore: event.data.best_score,
          code: event.data.best_generated_code,
          potentialIssues: event.data.potential_issues,
        });
        break;

      case "error":
        if (event.model) {
          const errorModel = event.model;
          setResults((prev) => {
            const currentResult = prev[errorModel];
            if (!currentResult) return prev;
            return {
              ...prev,
              [errorModel]: {
                ...currentResult,
                status: "error",
                error: event.message,
              },
            };
          });

          setWarnings((prev) => [
            ...prev,
            {
              id: `error-${errorModel}-${Date.now()}`,
              type: "model",
              message: event.message,
              model: errorModel,
            },
          ]);
        } else {
          setError(event.message);
        }
        break;

      case "complete":
        setIsComplete(true);
        break;
    }
  };

  const handleNewEvaluation = () => {
    router.push("/");
  };

  if (!prompt || models.length === 0) {
    return (
      <main className="flex min-h-screen w-full flex-col items-center justify-center gap-6 py-20 px-16 max-w-4xl mx-auto">
        <h1 className="text-4xl font-serif">No Evaluation Data</h1>
        <p className="text-muted-foreground">
          Please start an evaluation from the home page.
        </p>
        <Button onClick={handleNewEvaluation}>Go to Home</Button>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen w-full flex-col items-center gap-8 py-20 px-16 max-w-6xl mx-auto">
      <div className="w-full flex flex-col items-center gap-4">
        <h1 className="text-6xl font-serif">Evaluation Results</h1>
        <p className="text-muted-foreground text-center max-w-2xl">{prompt}</p>
      </div>

      {error && (
        <div className="w-full p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="w-full space-y-6">
        <h2 className="text-2xl font-semibold">Model Outputs</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {models.map((model) => {
            const result = results[model];
            if (!result) return null;
            return <ModelOutputCard key={model} result={result} />;
          })}
        </div>
      </div>

      {recommendation && (
        <div className="w-full space-y-4">
          <h2 className="text-2xl font-semibold">Our Recommendation</h2>
          <RecommendationSection recommendation={recommendation} />
        </div>
      )}

      {warnings.length > 0 && (
        <div className="w-full space-y-4">
          <WarningsSection warnings={warnings} />
        </div>
      )}

      <div className="w-full flex justify-center pt-6">
        <Button size="lg" asChild>
          <Link href="/">New Evaluation</Link>
        </Button>
      </div>

      {!isComplete && (
        <div className="fixed bottom-6 right-6 bg-white border rounded-lg shadow-lg p-4 flex items-center gap-3">
          <svg
            className="animate-spin h-5 w-5 text-primary"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <span className="text-sm font-medium">Processing...</span>
        </div>
      )}
    </main>
  );
}
