"""CLI tests."""

from kdp_category_picker.cli import main


def test_cli_browse(capsys):
    assert main(["browse"]) == 0
    out = capsys.readouterr().out
    assert "Top-level Amazon KDP categories" in out


def test_cli_search(capsys):
    assert main(["search", "python"]) == 0
    out = capsys.readouterr().out
    assert "Python" in out


def test_cli_tree(capsys):
    assert main(["tree", "Computers & Technology"]) == 0
    out = capsys.readouterr().out
    assert "Python" in out


def test_cli_save_and_picks(tmp_path, monkeypatch, capsys):
    import kdp_category_picker.store as stmod

    monkeypatch.setattr(stmod, "DEFAULT_STORE_PATH", tmp_path / "picks.json")
    assert (
        main(
            [
                "save",
                "Computers",
                "&",
                "Technology",
                ">",
                "Programming",
                ">",
                "Programming Languages",
                ">",
                "Python",
            ]
        )
        == 0
    )
    assert main(["picks"]) == 0
    out = capsys.readouterr().out
    assert "Python" in out


def test_cli_validate(capsys):
    assert (
        main(
            [
                "validate",
                "--category",
                "Computers & Technology > Programming > Programming Languages > Python",
                "--title",
                "Learn Python",
                "--keywords",
                "python",
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "Fit score" in out


def test_cli_export(tmp_path, monkeypatch, capsys):
    import kdp_category_picker.store as stmod

    monkeypatch.setattr(stmod, "DEFAULT_STORE_PATH", tmp_path / "picks.json")
    main(
        [
            "save",
            "Computers",
            "&",
            "Technology",
            ">",
            "Programming",
            ">",
            "Programming Languages",
            ">",
            "Python",
        ]
    )
    out_csv = tmp_path / "picks.csv"
    assert main(["export", str(out_csv)]) == 0
    assert out_csv.exists()
    content = out_csv.read_text()
    assert "Python" in content
