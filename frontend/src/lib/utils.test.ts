import { describe, it, expect } from "vitest";
import { cn, formatCurrency, formatDate } from "@/lib/utils";

describe("utils", () => {
  it("merges class names", () => {
    expect(cn("px-2", "py-1")).toBe("px-2 py-1");
    expect(cn("px-2", undefined, "py-1")).toBe("px-2 py-1");
  });

  it("formats currency", () => {
    expect(formatCurrency(1000)).toBe("$1,000");
  });

  it("formats date", () => {
    const formatted = formatDate("2026-01-15");
    expect(formatted).toContain("2026");
  });
});

describe("API URL", () => {
  it("has default API URL", () => {
    const url = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    expect(url).toContain("/api/v1");
  });
});
