"""Static installer tests for service update behavior."""

from pathlib import Path


INSTALL_SH = Path(__file__).resolve().parents[1] / "install.sh"
INSTALL_TEXT = INSTALL_SH.read_text()


def test_installer_detects_current_and_legacy_service_units():
    """Local installs reuse the detected server service instead of duplicating it."""
    assert 'SERVICE_NAME="aeo-ptt"' in INSTALL_TEXT
    assert 'LEGACY_SERVICE_NAME="stt-service"' in INSTALL_TEXT
    assert "installed_service_name()" in INSTALL_TEXT
    assert "/etc/systemd/system/$LEGACY_SERVICE_NAME.service" in INSTALL_TEXT


def test_service_setup_updates_and_restarts_detected_service_name():
    """Existing service setup updates/restarts whichever service was detected."""
    assert 'write_service_file "$service_name"' in INSTALL_TEXT
    assert 'sudo systemctl restart "$service_name"' in INSTALL_TEXT
    assert 'ExecStart=$HOME/.local/bin/uv run aeo-ptt-server' in INSTALL_TEXT
    assert 'SyslogIdentifier=$service_name' in INSTALL_TEXT


def test_uninstall_removes_detected_service_unit():
    """Uninstall path removes the same current-or-legacy service unit it detected."""
    assert 'sudo systemctl stop "$service_name"' in INSTALL_TEXT
    assert 'sudo systemctl disable "$service_name"' in INSTALL_TEXT
    assert 'sudo rm -f "/etc/systemd/system/$service_name.service"' in INSTALL_TEXT


def test_installer_does_not_hardcode_local_user_home():
    """Tracked installer must stay portable."""
    assert "/home/steve" not in INSTALL_TEXT
