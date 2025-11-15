import { z } from "zod";
import { MODELS, METRICS } from "./consts";

const modelValues = MODELS.map((m) => m.value);
const metricValues = METRICS.map((m) => m.value);

export const evaluateRequest = z.object({
  prompt: z
    .string()
    .min(5, "The prompt needs to be at least 5 characters long"),
  models: z.array(z.enum(modelValues)),
  metrics: z.array(z.enum(metricValues)),
});

export type EvaluateRequest = z.infer<typeof evaluateRequest>;
