---
name: castra
description: Castra execution posture harness manager. Use when managing checkpoints, inspecting or closing open loops, or checking command safety with the Castra Guardian classifier.
user-invocable: true
argument-hint: "[checkpoint | status | openloops | guardian <command>]"
---

# Castra Execution Posture Harness

Castra enforces an execution-forward posture, ensuring that coding agents do not stop one step early, maintain evidence-backed verification, and prevent unintended destructive actions.

## Available Actions

### 1. Checkpoint Progress (`checkpoint`)
Save the current progress so it survives across context windows or turns:
```bash
python C:\Users\JIN\.castra\scripts\castra_notes.py checkpoint --goal "My Goal" --progress "Completed phase 1" --next "Phase 2"
```

To read recent checkpoints:
```bash
python C:\Users\JIN\.castra\scripts\castra_notes.py read
```

### 2. Manage Open Loops (`openloops`)
Open loops represent unverified work, pending checks, or background tasks that must be resolved before a turn ends.
- **Add open loop**:
  ```powershell
  Add-Content -Path .castra/openloops -Value "[verify] check test suite output"
  ```
- **Inspect open loops**:
  ```powershell
  Get-Content -Path .castra/openloops
  ```
- **Close open loop**: Remove the completed line from `.castra/openloops`.

### 3. Guardian Risk Classifier (`guardian`)
Check any shell command before running:
```bash
python C:\Users\JIN\.castra\scripts\castra_guardian.py "git push --force"
```
- Exit 0: `not_required` (safe to run)
- Exit 2: `confirm_at_action` (requires immediate confirmation)
- Exit 3: `hand_off` (destructive/secret; agent must not run; user runs manually)

## Model Posture (Gemini 3.8)
When running on Gemini 3.8, Castra acts as an execution gate:
- Finish reversible work before reporting.
- Never delegate reversible tasks to the user ("you run it").
- Always execute and provide terminal evidence.
