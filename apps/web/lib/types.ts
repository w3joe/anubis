import { METRICS, MODELS } from "./consts";

export type Model = (typeof MODELS)[number]["value"];
export type Metric = (typeof METRICS)[number]["value"];
export type Option<TValue extends string> = { value: TValue; label: string };

// Stream Event Types
export type GenerationStartEvent = {
  type: "generation_start";
  model: Model;
};

export type CodeChunkEvent = {
  type: "code_chunk";
  model: Model;
  chunk: string;
};

export type GenerationCompleteEvent = {
  type: "generation_complete";
  model: Model;
  success: boolean;
  execution_time_ms: number;
};

export type EvaluationResultEvent = {
  type: "evaluation_result";
  model: Model;
  overall_score: number;
  metrics: Record<Metric, { score: number; notes: string }>;
  notes: {
    pros: string[];
    cons: string[];
  };
};

export type SummaryEvent = {
  type: "summary";
  data: {
    total_models_tested: number;
    successful_evaluations: number;
    failed_evaluations: number;
    best_model: Model;
    best_score: number;
    best_generated_code: string;
    potential_issues: string;
  };
  ranking: Array<{
    rank: number;
    model: Model;
    score: number;
  }>;
};

export type CompleteEvent = {
  type: "complete";
};

export type ErrorEvent = {
  type: "error";
  message: string;
  model?: Model;
};

export type StreamEvent =
  | GenerationStartEvent
  | CodeChunkEvent
  | GenerationCompleteEvent
  | EvaluationResultEvent
  | SummaryEvent
  | CompleteEvent
  | ErrorEvent;

// Model Result Types
export type ModelStatus = "pending" | "processing" | "complete" | "error";

export type EvaluationMetrics = Record<
  Metric,
  { score: number; notes: string }
>;

export type ModelResult = {
  model: Model;
  status: ModelStatus;
  code: string;
  executionTime?: number;
  overallScore?: number;
  metrics?: EvaluationMetrics;
  pros?: string[];
  cons?: string[];
  error?: string;
};

// Recommendation Types
export type Recommendation = {
  bestModel: Model;
  bestScore: number;
  code: string;
  potentialIssues: string;
};

// Warning Types
export type Warning = {
  id: string;
  type: "model" | "code_quality";
  message: string;
  model?: Model;
};
