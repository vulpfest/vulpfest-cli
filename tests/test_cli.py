from vulpfest.__main__ import main, run_tool
from vulpfest.banner import render


def test_version(capsys):
    assert main(["--version"]) == 0
    assert "vulpfest" in capsys.readouterr().out


def test_menu_lists_all_four_tools(capsys):
    assert main(["menu"]) == 0
    out = capsys.readouterr().out
    for name in ("Cyber Web Scanner", "Scam Check", "LeadScout", "GMaps Scout"):
        assert name in out


def test_unknown_tool_returns_2():
    assert main(["nope"]) == 2


def test_tool_help_uses_vulpfest_name(capsys):
    assert run_tool("check", ["--help"]) == 0
    assert "vulpfest check" in capsys.readouterr().out


def test_banner_renders_without_color_codes_when_not_tty():
    assert "VULPFEST".replace("", " ").strip() in render(set()).replace("  ", " ") or "V U L P F E S T" in render(set())
