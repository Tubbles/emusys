#!/usr/bin/env python3

import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="compile and run")
    parser.add_argument(
        "-w", "--clean-conan-source", action="store_true", help="clean conan cache, including sources (seldomly usable)")
    parser.add_argument(
        "-d", "--clean-conan", action="store_true", help="clean conan cache, keeping sources (seldomly usable)")
    parser.add_argument(
        "-c", "--clean-cmake", action="store_true", help="regenerate cmake")
    parser.add_argument(
        "-r", "--clean", action="store_true", help="clean build first")
    parser.add_argument(
        "-n", "--no-run", action="store_true", help="do not run after compile")
    parser.add_argument(
        "-b", "--build-dir", default="build", type=str, nargs="?", help="directory to place the build output")
    parser.add_argument(
        "extras", metavar="ARGS", type=str, nargs="*", help="optional arguments for the executable")

    args = parser.parse_args()
    mydir = os.path.dirname(os.path.realpath(__file__))
    builddir = os.path.join(mydir, args.build_dir)

    if args.clean_conan_source:
        os.system("conan remove \"*\" -s -b -p -f")
        os.system(f"cmake -S . -B {builddir} -DCMAKE_BUILD_TYPE=Release")

    if args.clean_conan:
        os.system("conan remove \"*\" -b -p -f")
        os.system(f"cmake -S . -B {builddir} -DCMAKE_BUILD_TYPE=Release")

    if args.clean_cmake:
        os.system(f"rm -fr {builddir}")

    if not os.path.isdir(f"{builddir}"):
        os.system(f"cmake -S . -B {builddir} -DCMAKE_BUILD_TYPE=Release")

    if args.clean:
        os.system(f"cd {builddir} && make clean")

    if args.no_run:
        os.system(f"cd {builddir} && make")
    else:
        os.system(
            f"cd {builddir} && make && ./bin/emusys {' '.join(args.extras)}")


if __name__ == "__main__":
    main()
