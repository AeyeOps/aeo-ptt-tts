# AEO Push-to-Talk & Text-to-Speech

GPU-accelerated voice I/O for Linux workstations.

## Components

| Package | Status | Description |
|---------|--------|-------------|
| **aeo-ptt** | Active | Speech-to-text with system-wide hotkey (Ctrl+Super) |
| **tts-service** | Planned | Low-latency text-to-speech |

## Quick Start (PTT)

```bash
curl -fsSL https://raw.githubusercontent.com/AeyeOps/aeo-ptt-tts/main/packages/aeo-ptt/install.sh | bash
```

See [packages/aeo-ptt/README.md](packages/aeo-ptt/README.md) for full documentation.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AEO Voice I/O                            │
├─────────────────────────────────────────────────────────────┤
│  PTT (Speech-to-Text)   │  TTS (Text-to-Speech) - planned   │
│  ─────────────────────  │  ──────────────────────────────   │
│  Audio → Text           │  Text → Audio                     │
│  Ctrl+Super hotkey      │  Low-latency streaming            │
│  NVIDIA Parakeet        │  (model TBD)                      │
└─────────────────────────────────────────────────────────────┘
```

## Requirements

- NVIDIA GPU with CUDA support
- Ubuntu/Debian-based Linux
- Python 3.12.3+

## License

MIT
