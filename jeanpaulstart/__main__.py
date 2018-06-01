import sys
import logging
import argparse
import jeanpaulstart


def process_args():
    parser = argparse.ArgumentParser(description="Jean-Paul Start - Cube's Launcher")
    parser.add_argument(
        '-j',
        '--json',
        type=str,
        help="JSON batch data"
    )
    parser.add_argument(
        '-n',
        '--not-normalized',
        action='store_true',
        help="Use if JSON data has not been normalized by jeanpaulstart"
    )
    parser.add_argument(
        '-f',
        '--filepath',
        type=str,
        help="Filepath to batch (.json / .yml)"
    )
    parse_args = parser.parse_args()
    return parse_args


if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    args = process_args()
    jeanpaulstart.load_plugins()

    status = jeanpaulstart.OK

    if args.json:
        status = jeanpaulstart.run_from_json(args.json, not args.not_normalized)

    elif args.filepath:
        status = jeanpaulstart.run_from_filepath(args.filepath)

    if status == jeanpaulstart.OK or status == jeanpaulstart.ERROR_IGNORED:
        exit_code = 0
    else:
        exit_code = status

    logging.info("Exit code is '{exit_code}'".format(exit_code=exit_code))
    sys.exit(exit_code)
