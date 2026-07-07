# Service Boundary Options

Generated from final architecture artifacts. This file provides forward-engineering options; it does not choose a future technology stack.

## Current Architecture Baseline

Detected architecture pattern: Layered Monolith.

The current evidence shows shared deployables, shared dependencies, and candidate module boundaries. Therefore service boundaries should be selected only after confirming ownership, data access, and call-flow behavior.

## Option A - Preserve As Modular Monolith First

Use when the team needs modernization without immediate service extraction.

Recommended when:

- module boundaries are still candidate-level
- data ownership is shared or unclear
- call flows are partial
- release risk must be minimized

Useful candidates to modularize internally first: none detected.

## Option B - Extract Low-Coupling Interface-Backed Capabilities

Use when a capability has clear interfaces, low coupling, and limited risk evidence.

Candidate capabilities:

- none detected

## Option C - Stabilize Shared Data/Infrastructure Before Extraction

Use when data access or infrastructure components are shared across capabilities.

Capabilities to keep internal until ownership is confirmed:

- none detected

## Option D - Defer High-Risk / Weak Boundary Candidates

Poor first extraction candidates:

- CAP-001 Catalog: weak modules 1, risks 3, coupling 13
- CAP-002 Identity: weak modules 1, risks 1, coupling 8
- CAP-004 Admin: weak modules 1, risks 1, coupling 3
- CAP-005 Basket: weak modules 1, risks 1, coupling 9
- CAP-006 Controllers: weak modules 1, risks 1, coupling 7
- CAP-007 Order: weak modules 1, risks 1, coupling 4
- CAP-013 Data: weak modules 1, risks 3, coupling 5

## Recommended Enterprise Use

Start with Option A as a stabilization path, use Option B only for low-coupling candidates, and defer Option D candidates until open questions and partial flows are resolved.
