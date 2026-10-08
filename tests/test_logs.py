from pysyskit.modules.logs import analyze_logs


def test_log_analysis(tmp_path):

    log_file = tmp_path / "auth.log"

    log_file.write_text(
        "Failed password for invalid user admin "
        "from 192.0.2.10 port 22 ssh2\n"
        "Accepted publickey for user "
        "from 192.0.2.11 port 22 ssh2\n",
        encoding="utf-8",
    )

    result = analyze_logs(
        (str(log_file),)
    )

    assert (
        result[
            "failed_authentication_attempts"
        ]
        == 1
    )

    assert (
        result[
            "successful_authentication_events"
        ]
        == 1
    )

    assert (
        result["invalid_user_events"]
        == 1
    )
