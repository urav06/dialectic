#!/usr/bin/env python3
"""CLI entry point for debate operations.

This module makes the package executable via:
  python3 /path/to/debate_ops/__main__.py <command>

The path setup below ensures absolute imports work when run as a script.
"""

import json
import sys
from pathlib import Path

# Add package parent directory to sys.path for absolute imports
# This allows: python3 .claude/skills/debate-orchestrator/debate_ops/__main__.py
_package_dir = Path(__file__).resolve().parent.parent
if str(_package_dir) not in sys.path:
    sys.path.insert(0, str(_package_dir))

from debate_ops.debater import process_debater
from debate_ops.judge import process_judge
from debate_ops.state import update_debate_state


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"success": False, "error": "Usage: python3 -m debate_ops <command> <args...>"}
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "process-exchange":
            # New command: processes both sides and updates state
            # Usage: python3 -m debate_ops process-exchange <debate> <exchange> --prop-file <path> --opp-file <path>
            if len(sys.argv) != 8:
                print(
                    json.dumps(
                        {
                            "success": False,
                            "error": "Usage: process-exchange <debate> <exchange> --prop-file <path> --opp-file <path>",
                        }
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)

            debate = sys.argv[2]
            exchange = int(sys.argv[3])

            # Extract file paths
            try:
                prop_file_idx = sys.argv.index("--prop-file")
                prop_file_path = Path(sys.argv[prop_file_idx + 1])
                opp_file_idx = sys.argv.index("--opp-file")
                opp_file_path = Path(sys.argv[opp_file_idx + 1])
            except (ValueError, IndexError):
                print(
                    json.dumps({"success": False, "error": "Both --prop-file and --opp-file required"}),
                    file=sys.stderr,
                )
                sys.exit(1)

            # Process proposition side
            prop_output = prop_file_path.read_text()
            result_prop = process_debater(
                debate=debate,
                side='proposition',
                exchange=exchange,
                output=prop_output,
            )

            if not result_prop.success:
                prop_file_path.unlink(missing_ok=True)
                opp_file_path.unlink(missing_ok=True)
                print(json.dumps({
                    "success": False,
                    "side": "proposition",
                    "errors": result_prop.errors,
                    "warnings": result_prop.warnings,
                }), file=sys.stderr)
                sys.exit(1)

            # Process opposition side
            opp_output = opp_file_path.read_text()
            result_opp = process_debater(
                debate=debate,
                side='opposition',
                exchange=exchange,
                output=opp_output,
            )

            if not result_opp.success:
                prop_file_path.unlink(missing_ok=True)
                opp_file_path.unlink(missing_ok=True)
                print(json.dumps({
                    "success": False,
                    "side": "opposition",
                    "errors": result_opp.errors,
                    "warnings": result_opp.warnings,
                }), file=sys.stderr)
                sys.exit(1)

            # Both sides processed successfully - update state
            update_debate_state(debate, current_phase='awaiting_judgment')

            # Clean up temp files
            prop_file_path.unlink(missing_ok=True)
            opp_file_path.unlink(missing_ok=True)

            # Output combined result
            output_dict = {
                "success": True,
                "argument_id": {
                    "proposition": result_prop.argument_id,
                    "opposition": result_opp.argument_id,
                },
                "warnings": (result_prop.warnings or []) + (result_opp.warnings or []) or None,
            }
            print(json.dumps(output_dict, indent=2))
            sys.exit(0)

        elif command == "process-judge":
            # Usage: python3 -m debate_ops process-judge <debate> --json-file <path>
            if len(sys.argv) != 5:
                print(
                    json.dumps(
                        {
                            "success": False,
                            "error": "Usage: process-judge <debate> --json-file <path>",
                        }
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                json_file_idx = sys.argv.index("--json-file")
                json_file_path = Path(sys.argv[json_file_idx + 1])
                output = json_file_path.read_text()
            except (ValueError, IndexError):
                print(
                    json.dumps({"success": False, "error": "--json-file parameter required"}),
                    file=sys.stderr,
                )
                sys.exit(1)

            result = process_judge(debate=sys.argv[2], output=output)

            # Clean up temp file
            json_file_path.unlink(missing_ok=True)

            # Output result
            output_dict = {
                "success": result.success,
                "argument_id": result.argument_id,
                **(
                    {"score": result.score}
                    if hasattr(result, "score") and result.score
                    else {}
                ),
                **(
                    {"rescored": result.rescored}
                    if hasattr(result, "rescored") and result.rescored
                    else {}
                ),
                **({"errors": result.errors} if result.errors else {}),
                **({"warnings": result.warnings} if result.warnings else {}),
            }
            print(json.dumps(output_dict, indent=2))
            sys.exit(0 if result.success else 1)

        else:
            print(
                json.dumps({"success": False, "error": f"Unknown command: {command}"}),
                file=sys.stderr,
            )
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
