"""Tests for paste-based transcript output."""

from unittest import mock

from aeo_ptt import client


def test_paste_text_x11_copies_text_then_sends_single_paste_chord(monkeypatch):
    """Paste output uses clipboard plus one Ctrl+V, not per-character typing."""
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")
    calls = []

    def fake_run(args, input=None, check=False):
        calls.append((args, input, check))
        return mock.Mock(returncode=0)

    monkeypatch.setattr(client.subprocess, "run", fake_run)

    client.paste_text("hello world")

    assert calls == [
        (["xclip", "-selection", "clipboard"], b"hello world", True),
        (["xdotool", "key", "--clearmodifiers", "ctrl+v"], None, True),
    ]


def test_paste_text_does_not_send_paste_when_clipboard_copy_fails(monkeypatch):
    """Paste output does not press Ctrl+V when clipboard copy is unavailable."""
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")
    calls = []

    def fake_run(args, input=None, check=False):
        calls.append((args, input, check))
        if args[0] == "xclip":
            raise FileNotFoundError("xclip")
        return mock.Mock(returncode=0)

    monkeypatch.setattr(client.subprocess, "run", fake_run)

    client.paste_text("hello world")

    assert calls == [(["xclip", "-selection", "clipboard"], b"hello world", True)]
