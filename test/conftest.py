"""Harness-wide pytest configuration."""


def pytest_addoption(parser):
    parser.addoption(
        "--show-model-output",
        action="store_true",
        default=False,
        help="Print each scenario's raw model output to the console (debug); "
        "prints live for every test, no -s needed.",
    )
