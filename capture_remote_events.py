#!/usr/bin/env python3
"""Save Toshiba commands caused by the original remote from ESPHome logs."""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


EVENT_RE = re.compile(
    r"REMOTE_EVENT command=(?P<command>(?:0x)?[0-9A-Fa-f]{2}) "
    r"value=(?P<value>(?:0x)?[0-9A-Fa-f]{2}) frame=(?P<frame>.+?)\s*$"
)

COMMAND_NAMES = {
    0x80: "POWER_STATE",
    0x87: "POWER_SELECT",
    0xA0: "FAN_MODE",
    0xA3: "SWING_MODE",
    0xB0: "MODE",
    0xB3: "TARGET_TEMPERATURE",
    0xBB: "ROOM_TEMPERATURE",
    0xBE: "OUTDOOR_TEMPERATURE",
    0xC7: "IONIZER",
    0xDE: "WIFILED1",
    0xDF: "WIFILED2",
    0xE4: "IDU_STATUS",
    0xE5: "ODU_STATUS",
    0xF7: "SPECIAL_MODE",
}


def parse_event(line: str) -> dict[str, object] | None:
    match = EVENT_RE.search(line)
    if match is None:
        return None

    command = int(match["command"], 16)
    value = int(match["value"], 16)
    return {
        "captured_at": datetime.now().astimezone().isoformat(timespec="milliseconds"),
        "command": f"0x{command:02X}",
        "command_name": COMMAND_NAMES.get(command, "UNKNOWN"),
        "value": f"0x{value:02X}",
        "frame": match["frame"],
    }


def self_test() -> None:
    event = parse_event(
        "[I][toshiba-capture:620]: REMOTE_EVENT command=80 value=31 "
        "frame=02.00.03.10.00.00.07.01.30.01.00.02.80.31.01"
    )
    assert event is not None
    assert event["command_name"] == "POWER_STATE"
    assert event["value"] == "0x31"
    print("Remote event reader self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read ESPHome logs from stdin and save remote-control events as JSON Lines."
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=Path("toshiba-remote-events.jsonl"),
        help="output JSONL file (default: toshiba-remote-events.jsonl)",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    count = 0
    print(f"Capturing remote events to {args.output}; stop with Ctrl-C.", file=sys.stderr)
    try:
        with args.output.open("a", encoding="utf-8") as output:
            for line in sys.stdin:
                event = parse_event(line)
                if event is None:
                    continue
                output.write(json.dumps(event, ensure_ascii=False) + "\n")
                output.flush()
                count += 1
                print(
                    f'{event["captured_at"]} {event["command_name"]} '
                    f'{event["command"]} = {event["value"]}'
                )
    except KeyboardInterrupt:
        pass

    print(f"Captured {count} remote events.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
