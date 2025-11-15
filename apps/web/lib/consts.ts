import { Option } from "./types";

export const MODELS = [
  { value: "gemini-2.5-pro", label: "Gemini 2.5 Pro" },
  { value: "gemini-2.5-flash", label: "Gemini 2.5 Flash" },
  { value: "gemini-2.5-flash-lite", label: "Gemini 2.5 Flash Lite" },
  { value: "gemma-3-1b-it", label: "Gemini 3 1B" },
] as const satisfies Option<string>[];

export const METRICS = [
  { value: "time_complexity", label: "Time Complexity" },
  { value: "readability", label: "Readability" },
  { value: "consistency", label: "Consistency" },
  { value: "code_documentation", label: "Code Documentation" },
  { value: "external_dependencies", label: "External Dependencies" },
] as const satisfies Option<string>[];
