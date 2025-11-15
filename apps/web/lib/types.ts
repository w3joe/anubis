import { METRICS, MODELS } from "./consts";

export type Model = (typeof MODELS)[number]["value"];
export type Metric = (typeof METRICS)[number]["value"];
export type Option<TValue extends string> = { value: TValue; label: string };
