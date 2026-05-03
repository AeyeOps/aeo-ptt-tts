"""Tests for Shift-modified PTT paste gesture."""

from aeo_ptt.ptt import EvdevHotkeyListener, PTTController


class _DummyTask:
    def cancel(self):
        pass


class _FakeListener:
    def __init__(self, paste_requested=False):
        self.paste_requested = paste_requested
        self.on_activate = None
        self.on_deactivate = None

    async def start(self):
        pass

    def stop(self):
        pass


def test_ptt_stop_callback_receives_paste_requested_from_listener(monkeypatch):
    """PTTController passes the listener paste flag to stop callbacks."""
    fake_listener = _FakeListener(paste_requested=True)
    controller = PTTController(listener=fake_listener)
    stops = []

    def fake_create_task(coro):
        coro.close()
        return _DummyTask()

    monkeypatch.setattr("aeo_ptt.ptt.asyncio.create_task", fake_create_task)
    monkeypatch.setattr(controller, "_play_sound", lambda sound_type: None)
    controller.set_callbacks(on_start=lambda: None, on_stop=lambda paste: stops.append(paste))

    controller._on_hotkey_activate()
    controller._on_hotkey_deactivate()

    assert stops == [True]


def test_evdev_listener_remembers_shift_seen_during_active_hotkey():
    """Shift can be pressed and released before base-key release and still request paste."""
    deactivations = []
    listener = EvdevHotkeyListener(
        on_activate=lambda: None,
        on_deactivate=lambda: deactivations.append(listener.paste_requested),
        hotkey=["LEFTCTRL", "LEFTMETA"],
    )
    listener._hotkey_codes = {1, 2}
    listener._shift_codes = {3, 4}
    listener._pressed_keys_by_device = {"kbd": {1, 2}}

    listener._check_hotkey()
    assert listener.paste_requested is False

    listener._pressed_keys_by_device = {"kbd": {1, 2, 3}}
    listener._check_hotkey()
    assert listener.paste_requested is True

    listener._pressed_keys_by_device = {"kbd": {1, 2}}
    listener._check_hotkey()
    assert listener.paste_requested is True

    listener._pressed_keys_by_device = {"kbd": {1}}
    listener._check_hotkey()

    assert deactivations == [True]
