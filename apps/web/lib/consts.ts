import { Option } from "./types";

export const MODELS = [
  { value: "gemini-2.5-pro-latest", label: "Gemini 2.5 Pro Latest" },
  { value: "gemini-2.5-pro", label: "Gemini 2.5 Pro" },
  { value: "gemini-2.5-flash", label: "Gemini 2.5 Flash" },
  { value: "gemini-2.5-flash-lite", label: "Gemini 2.5 Flash Lite" },
  { value: "gemma-3-1b-it", label: "Gemma 3 1B" },
  { value: "gemini-2.0-flash-lite", label: "Gemini 2.0 Flash Lite" },
  {
    value: "gemini-2.0-flash-thinking-exp",
    label: "Gemini 2.0 Flash Thinking Exp",
  },
  { value: "learnlm-2.0-flash-experimental", label: "LearnLM 2.0 Flash Exp" },
] as const satisfies Option<string>[];

export const METRICS = [
  { value: "time_complexity", label: "Time Complexity" },
  { value: "readability", label: "Readability" },
  { value: "consistency", label: "Consistency" },
  { value: "code_documentation", label: "Code Documentation" },
  { value: "external_dependencies", label: "External Dependencies" },
] as const satisfies Option<string>[];
