"""Tests for paste-based transcript output."""

from unittest import mock

from aeo_ptt import client


def test_paste_text_x11_copies_text_then_sends_single_paste_chord(monkeypatch):
    """Paste output uses clipboard plus one Ctrl+V, not per-character typing."""
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")
    calls = []

    def fake_run(args, input=None, check=False, capture_output=False, text=False):
        calls.append((args, input, check, capture_output, text))
        if args == ["xdotool", "getactivewindow"]:
            return mock.Mock(stdout="12345\n", returncode=0)
        if args[:3] == ["xprop", "-id", "12345"]:
            return mock.Mock(stdout='WM_CLASS(STRING) = "chromium", "Chromium"\n', returncode=0)
        return mock.Mock(returncode=0)

    monkeypatch.setattr(client.subprocess, "run", fake_run)

    client.paste_text("hello world")

    assert calls == [
        (["xclip", "-selection", "clipboard"], b"hello world", True, False, False),
        (["xdotool", "getactivewindow"], None, True, True, True),
        (["xprop", "-id", "12345", "WM_CLASS"], None, True, True, True),
        (["xdotool", "key", "--clearmodifiers", "ctrl+v"], None, True, False, False),
    ]


def test_paste_text_x11_uses_terminal_paste_chord_for_terminal_window(monkeypatch):
    """Terminal windows use Ctrl+Shift+V so TUIs like Codex do not treat Ctrl+V as image paste."""
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")
    calls = []

    def fake_run(args, input=None, check=False, capture_output=False, text=False):
        calls.append((args, input, check, capture_output, text))
        if args == ["xdotool", "getactivewindow"]:
            return mock.Mock(stdout="12345\n", returncode=0)
        if args[:3] == ["xprop", "-id", "12345"]:
            return mock.Mock(
                stdout='WM_CLASS(STRING) = "gnome-terminal-server", "Gnome-terminal"\n',
                returncode=0,
            )
        return mock.Mock(returncode=0)

    monkeypatch.setattr(client.subprocess, "run", fake_run)

    client.paste_text("hello tmux")

    assert calls == [
        (["xclip", "-selection", "clipboard"], b"hello tmux", True, False, False),
        (["xdotool", "getactivewindow"], None, True, True, True),
        (["xprop", "-id", "12345", "WM_CLASS"], None, True, True, True),
        (["xdotool", "key", "--clearmodifiers", "ctrl+shift+v"], None, True, False, False),
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
