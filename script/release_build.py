#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import *

import json
import argparse


def write_text(path: str, content: str):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def replace_pyproject_toml(version: str):
    import toml
    data = toml.load(PYPROJECT_TOML)
    data["project"]["version"] = version
    with open(PYPROJECT_TOML, "w", encoding="utf-8") as file:
        toml.dump(data, file)
    print("已修改pyproject.toml版本号！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", required=False, help="版本号")
    args = parser.parse_args()
    version = args.version

    replace_pyproject_toml(version)

    out = {
        "version": version,
    }

    out_path = os.path.join(ROOT, "script", "release_output.json")
    print("打包结果：", out)
    write_text(out_path, json.dumps(out, ensure_ascii=False, indent=4))
