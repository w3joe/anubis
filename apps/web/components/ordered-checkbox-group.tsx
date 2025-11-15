"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";

export interface OrderedCheckboxOption<TValue extends string = string> {
  value: TValue;
  label: string;
}

interface OrderedCheckboxGroupProps<TValue extends string = string> {
  options: OrderedCheckboxOption<TValue>[];
  id?: string;
  selectedValues?: TValue[];
  onChange?: (selectedValues: TValue[]) => void;
  className?: string;
}

export function OrderedCheckboxGroup<TValue extends string = string>({
  options,
  id = "checkboxes",
  selectedValues: controlledValues,
  onChange,
  className,
}: OrderedCheckboxGroupProps<TValue>) {
  const [internalValues, setInternalValues] = useState<TValue[]>([]);

  const isControlled = controlledValues !== undefined;
  const selectedValues = isControlled ? controlledValues : internalValues;

  const handleToggle = (value: TValue) => {
    let newValues: TValue[];

    if (selectedValues.includes(value)) {
      // Remove the value and maintain order of remaining items
      newValues = selectedValues.filter((v) => v !== value);
    } else {
      // Add the value at the end
      newValues = [...selectedValues, value];
    }

    if (!isControlled) {
      setInternalValues(newValues);
    }
    onChange?.(newValues);
  };

  const getOrderNumber = (value: TValue): number | null => {
    const index = selectedValues.indexOf(value);
    return index !== -1 ? index + 1 : null;
  };

  return (
    <div className={cn("flex flex-wrap gap-3", className)} id={id}>
      {options.map((option) => {
        const orderNumber = getOrderNumber(option.value);
        const isSelected = orderNumber !== null;

        return (
          <button
            key={option.value}
            type="button"
            onClick={() => handleToggle(option.value)}
            className={cn(
              "inline-flex items-center gap-2.5 rounded-md px-4 py-2.5",
              "text-sm font-medium transition-all cursor-pointer",
              "border shadow-sm",
              "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
              isSelected
                ? "bg-primary text-primary-foreground"
                : "bg-white/75 hover:bg-accent hover:text-accent-foreground"
            )}
          >
            <div
              className={cn(
                "flex items-center justify-center size-5 rounded border-2 transition-all",
                "font-semibold text-xs",
                isSelected
                  ? "bg-white text-primary border-white"
                  : "bg-transparent border-muted-foreground"
              )}
            >
              {isSelected ? orderNumber : ""}
            </div>
            <span>{option.label}</span>
          </button>
        );
      })}
    </div>
  );
}
