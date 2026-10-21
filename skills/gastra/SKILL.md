---
name: gastra
description: Gastra execution posture harness manager for Gemini & Antigravity. Use when managing checkpoints, inspecting or closing open loops, or checking command safety with the Gastra Guardian classifier.
user-invocable: true
argument-hint: "[checkpoint|read|budget|search|openloop]"
---

# Gastra — Gemini Adaptive System for Task Reliability & Agency

Gastra is the execution posture harness built specifically for Gemini models and Antigravity, enforcing the anti-premature hand-off principle, automated verification, and context checkpoint survival.

## Commands

### 1. Checkpoint Management
```bash
python C:\Users\JIN\.gastra\scripts\gastra_notes.py checkpoint --goal "..." --progress "..." --next "..."
python C:\Users\JIN\.gastra\scripts\gastra_notes.py read
python C:\Users\JIN\.gastra\scripts\gastra_notes.py budget
```

### 2. Open-Loop Protocol
Keep unfinished tasks tracked in `.gastra/openloops`:
- Add open loop: `echo "[verify] description" >> .gastra/openloops`
- Remove when verified.
