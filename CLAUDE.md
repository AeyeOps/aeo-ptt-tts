# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AEO PTT-TTS** provides GPU-accelerated voice I/O for Linux workstations:

- **stt-service** (`packages/stt-service/`) - Speech-to-text with system-wide hotkey
- **tts-service** (`packages/tts-service/`) - Text-to-speech (planned)

## Build & Development Commands

```bash
# Install all workspace dependencies
uv sync

# Install STT service with all extras
uv sync --package stt-service --all-extras

# Run tests
cd packages/stt-service && pytest tests/

# Run STT server (requires GPU)
packages/stt-service/scripts/stt-server.sh

# Run STT client in PTT mode
packages/stt-service/scripts/stt-client.sh --ptt

# After uv sync, CLI commands available in venv
stt-server   # Start STT server
stt-client   # Start PTT client
```

## Architecture

### Monorepo Structure
- `uv` workspace with Python 3.12.3+
- Root `pyproject.toml` defines workspace, packages in `packages/*`
- Build backend: hatchling

### STT Service Components (`packages/stt-service/src/stt_service/`)

| Module | Purpose |
|--------|---------|
| `server.py` | WebSocket server, session management, model inference |
| `client.py` | WebSocket PTT client, audio streaming, output modes |
| `ptt.py` | Push-to-Talk state machine, hotkey listeners |
| `transcriber.py` | ONNX-asr wrapper with Parakeet TDT model, GPU-only |
| `config.py` | Pydantic-settings configuration (env vars) |
| `protocol.py` | WebSocket message protocol |
| `tray.py` | System tray indicator |

### Key Design Decisions

1. **GPU-only, fail-fast**: No CPU fallback
2. **Environment-driven config**: All settings via env vars (prefix: `STT_`)
3. **Dual hotkey listeners**: evdev (desktop) vs terminal (Docker/SSH)

## Key Environment Variables

```bash
# Server
STT_SERVER_HOST=127.0.0.1
STT_SERVER_PORT=9876
STT_MODEL_PROVIDER=cuda

# Client
STT_CLIENT_OUTPUT_MODE=stdout  # stdout, type, clipboard
STT_PTT_HOTKEY='["LEFTCTRL", "LEFTMETA"]'
```

## Model Cache

```bash
# Parakeet ONNX models downloaded to:
~/.cache/onnx-asr/
```

## Coding Standards

### Shell Scripts
- Shebang: `#!/usr/bin/env bash`
- Safety: `set -euo pipefail`
- Lint with `shellcheck`

### Python
- Type hints required
- Pydantic for data models and configuration
- asyncio for concurrency

### Commits
- Imperative mood: `fix(stt-service): correct model path`
- No Co-Authored-By lines for AI

## Platform Notes

- **Target**: NVIDIA GB10 (ARM64) and x86_64 workstations
- **OS**: Ubuntu 22.04/24.04 LTS
- **ARM64 GPU**: Requires manual onnxruntime-gpu wheel
