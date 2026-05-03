# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2026-05-03

### Added
- Added a native Ctrl+Super+Shift paste gesture that copies the current
  transcript and sends a single paste chord for apps where simulated typing is
  unsuitable.
- Added local-checkout installer updates so `packages/aeo-ptt/install.sh -y`
  can refresh an existing install from the current repo checkout.

### Changed
- Updated installer service handling to reuse and refresh existing
  `aeo-ptt.service` or legacy `stt-service.service` instead of creating a
  duplicate service.
- Updated tray/client launch to restore the desktop session bus environment
  when needed for AppIndicator/StatusNotifier registration.
- Updated paste behavior to use Ctrl+Shift+V in terminal windows while keeping
  Ctrl+V in normal graphical applications.

### Verified
- Ctrl+Super+Shift paste was confirmed live in Codex under tmux, Claude Code,
  and regular graphical apps including LibreOffice Writer.

## [0.5.0] - 2026-01-25

### Changed
- Renamed package from `stt-service` to `aeo-ptt`
- Renamed Python module from `stt_service` to `aeo_ptt`
- Renamed CLI commands from `stt-server`/`stt-client` to `aeo-ptt-server`/`aeo-ptt-client`
- Renamed scripts to match new naming convention

## [0.1.0] - 2026-01-25

### Added
- Initial repository setup
- Migrated stt-service from ai-essentials repository
- Scaffold for future tts-service package
