#!/usr/bin/env python3
import subprocess
import sys
import json
import re

CONFIG_FILE_LOCATION = "/config.json"
CODE_LOCATION = "/code"
ECLIPSE_REGEX = re.compile(r'^(.*):([0-9]+):\s*(\w+):\s+(.*?)\s+\[([^\]]+)\]\s+\[([0-9]+)\]')


def print_issue(line: str):
    matches = ECLIPSE_REGEX.fullmatch(line)
    if matches is None:
        return
    (file, line, severity, message, check, level) = matches.group(1, 2, 3, 4, 5, 6)
    issue = {
        "type": "issue",
        "check_name": check,
        "description": message,
        "categories": ["Style"],
        "location": {
            "path": file,
            "lines": {
                "begin": int(line),
                "end": int(line)
            }
        }
    }
    json.dump(issue, sys.stdout)
    print("\0")


def run_cpplint(workspace, files, config):
    cmd = ["cpplint", "--output=eclipse", "--quiet", "--recursive"]
    if type(config) is dict:
        for option in config:
            if option in ["output", "quiet"]:
                continue
            cmd.append("--%s=%s" % (option, config[option]))
    else:
        print("Warning: 'config' should be an object but is %s" % type(config).__name__, file=sys.stderr)

    cmd.extend(files)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            output = e.output
        else:
            raise e

    if len(output):
        output = output.decode('utf-8')
        for line in output.splitlines():
            print_issue(line)


def main():
    config_file_path = CONFIG_FILE_LOCATION
    workspace_path = CODE_LOCATION
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    engine_config = config["config"]
    run_cpplint(workspace_path, config["include_paths"], engine_config)
    print("\0")
    pass


if __name__ == "__main__":
    main()
