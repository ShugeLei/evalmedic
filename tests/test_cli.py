import json

from evalmedic.cli import main


def test_cli_emits_json(capsys) -> None:
    exit_code = main(["diagnose", "examples/model_regression.json"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["abstained"] is False
    assert payload["ranked_causes"][0]["component"] == "model"

