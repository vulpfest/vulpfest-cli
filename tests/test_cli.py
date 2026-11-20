import pytest

from vulpfest.__main__ import main, run_tool


@pytest.fixture(autouse=True)
def english(monkeypatch):
    monkeypatch.setenv("VULPFEST_LANG", "en")


def test_version(capsys):
    assert main(["--version"]) == 0
    assert "vulpfest" in capsys.readouterr().out


def test_menu_lists_all_four_tools_in_english(capsys):
    assert main(["menu"]) == 0
    out = capsys.readouterr().out
    for name in ("Cyber Web Scanner", "Scam Check", "LeadScout", "GMaps Scout"):
        assert name in out
    assert "Free tools" in out and "V U L P F E S T" in out


def test_lang_flag_switches_to_indonesian(capsys):
    assert main(["--lang", "id", "menu"]) == 0
    assert "Alat gratis" in capsys.readouterr().out


def test_env_switches_to_indonesian(monkeypatch, capsys):
    monkeypatch.setenv("VULPFEST_LANG", "id")
    assert main(["menu"]) == 0
    assert "Alat gratis" in capsys.readouterr().out


def test_unknown_tool_returns_2():
    assert main(["nope"]) == 2


def test_tool_help_uses_vulpfest_name(capsys):
    assert run_tool("check", ["--help"]) == 0
    assert "vulpfest check" in capsys.readouterr().out


def test_menu_returns_after_a_tool(monkeypatch):
    import vulpfest.__main__ as m
    answers = iter(["2", "example.com/x.apk", "", "4", "coffee in Batam", "kafe.xlsx", "q"])
    calls = []
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    monkeypatch.setattr(m, "run_tool", lambda key, args, lang="en": calls.append((key, args)) or 0)
    assert m.interactive("en") == 0
    assert calls == [("check", ["example.com/x.apk"]), ("gmaps", ["coffee in Batam", "--out", "kafe.xlsx"])]


def test_empty_choice_quits(monkeypatch):
    import vulpfest.__main__ as m
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    assert m.interactive("en") == 0
