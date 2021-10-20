#!/usr/bin/env python3

import argparse
import subprocess  # nosec
import sys


def _print(message: str) -> None:
    print(message)
    sys.stdout.flush()


def main() -> None:
    """Get some logs to from k8s."""
    parser = argparse.ArgumentParser(description="Get some logs to from k8s.")
    parser.add_argument("--namespace", help="Namespace to be used")

    args = parser.parse_args()

    if args.namespace:
        subprocess.run(["kubectl", "config", "set-context", "--current", "--namespace=default"], check=True)

    _print("::group::Events")
    subprocess.run(["kubectl", "get", "events"], check=True)
    _print("::endgroup::")

    _print("::group::Deployments")
    subprocess.run(["kubectl", "get", "deployments", "--output=wide"], check=True)
    _print("::endgroup::")

    _print("::group::Pods")
    subprocess.run(["kubectl", "get", "pods", "--output=wide"], check=True)
    _print("::endgroup::")

    for name in (
        subprocess.run(["kubectl", "get", "pods", "--output=name"], check=True, stdout=subprocess.PIPE)
        .stdout.decode()
        .split("\n")
    ):
        if name:
            _print(f"::group::{name}: Describe")
            subprocess.run(["kubectl", "describe", name], check=True)
            _print("::endgroup::")

            for container in (
                subprocess.run(
                    ["kubectl", "get", name, "--output=jsonpath={.spec.initContainers[*].name}"],
                    check=True,
                    stdout=subprocess.PIPE,
                )
                .stdout.decode()
                .split("\n")
            ):
                if name:
                    _print(f"::group::{name} {container}: Logs")
                    subprocess.run(["kubectl", "logs", name, container], check=False)
                    _print("::endgroup::")

            for container in (
                subprocess.run(
                    ["kubectl", "get", name, "--output=jsonpath={.spec.containers[*].name}"],
                    check=True,
                    stdout=subprocess.PIPE,
                )
                .stdout.decode()
                .split("\n")
            ):
                _print(f"::group::{name} {container}: Logs")
                subprocess.run(["kubectl", "logs", name, container], check=False)
                _print("::endgroup::")


if __name__ == "__main__":
    main()
