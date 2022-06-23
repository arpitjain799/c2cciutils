import argparse
import sys

import yaml

import c2cciutils.lib.docker


def main() -> None:
    argparser = argparse.ArgumentParser(
        description="Update the versions of the dpkg packages installed in the images"
    )
    argparser.add_argument("--distribution", help="The default distribution code to be used")
    argparser.add_argument("--release", help="The default release version to be used")
    argparser.add_argument("images", help="The image to check", nargs="+")
    args = argparser.parse_args()

    versions_config = c2cciutils.lib.docker.get_versions_config()
    for image in args.images:
        c2cciutils.lib.docker.check_version(
            versions_config,
            image,
            check=False,
            default_distribution=args.distribution,
            default_release=args.release,
        )

    with open("ci/dpkg-versions.yaml", "w", encoding="utf-8") as versions_file:
        versions_file.write("# See repository list: https://repology.org/repositories/statistics\n\n")
        versions_file.write(yaml.dump(versions_config, Dumper=yaml.SafeDumper, default_flow_style=False))


if __name__ == "__main__":
    main()
