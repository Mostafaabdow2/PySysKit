from pysyskit.modules.security import (
    get_open_ports,
    inspect_accounts,
)


def test_open_ports_returns_list():

    result = get_open_ports()

    assert isinstance(result, list)


def test_accounts_structure():

    accounts = inspect_accounts()

    assert isinstance(accounts, list)

    if accounts:

        required = {
            "username",
            "uid",
            "gid",
            "shell",
            "severity",
            "indicators",
        }

        assert required <= accounts[0].keys()
