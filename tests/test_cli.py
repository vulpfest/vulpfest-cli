import pytest

from vulpfest.__main__ import main, run_tool


@pytest.fixture(autouse=True)
def english(monkeypatch, tmp_path):
    monkeypatch.setenv("VULPFEST_LANG", "en")
    monkeypatch.setenv("VULPFEST_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VULPFEST_OUT", str(tmp_path / "out"))
    monkeypatch.setenv("VULPFEST_NO_UPDATE_CHECK", "1")


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


def test_links_command(capsys):
    assert main(["links"]) == 0
    out = capsys.readouterr().out
    assert "www.vulpfest.com" in out and "instagram.com/vulpfest" in out


def test_menu_l_shows_links(monkeypatch, capsys):
    import vulpfest.__main__ as m
    answers = iter(["l", "q"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    assert m.interactive("en") == 0
    assert "x.com/Vulpfest" in capsys.readouterr().out


def test_bare_file_names_go_to_the_results_folder(tmp_path):
    from vulpfest.config import resolve_out
    assert resolve_out("kafe.xlsx") == str(tmp_path / "out" / "kafe.xlsx")
    assert resolve_out("sub/kafe.xlsx").replace("\\", "/") == "sub/kafe.xlsx"


def test_config_out_is_saved(monkeypatch, tmp_path):
    from vulpfest.config import out_dir
    monkeypatch.delenv("VULPFEST_OUT")
    assert main(["config", "out", str(tmp_path / "data")]) == 0
    assert out_dir() == (tmp_path / "data").resolve()


def test_version_compare():
    from vulpfest.update import newer
    assert newer("1.0.10", "1.0.9") and not newer("1.0.3", "1.0.3") and not newer(None, "1.0.3")


def test_completion_scripts(capsys):
    for shell, needle in (("powershell", "Register-ArgumentCompleter"), ("bash", "complete -F"), ("zsh", "compdef")):
        assert main(["completion", shell]) == 0
        assert needle in capsys.readouterr().out


def test_doctor_runs_offline(monkeypatch, capsys):
    import vulpfest.doctor as d
    monkeypatch.setattr(d, "fetch_latest", lambda timeout=3: None)
    assert d.doctor("en") in (0, 1)
    assert "vulpfest doctor" in capsys.readouterr().out


def test_unexpected_errors_are_friendly(monkeypatch, capsys):
    import vulpfest.__main__ as m
    def boom(argv=None):
        raise ValueError("boom")
    monkeypatch.setattr(m, "_main", boom)
    assert m.main([]) == 1
    err = capsys.readouterr().err
    assert "boom" in err and "issues/new" in err


def test_typo_suggestion(capsys):
    assert main(["d"]) == 2
    assert "Did you mean: vulpfest doctor?" in capsys.readouterr().out
    assert main(["chek"]) == 2
    assert "Did you mean: vulpfest check?" in capsys.readouterr().out
