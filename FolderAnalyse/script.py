"""
Ryan Pepper (2018)

This script contains the main entrypoint to the folder-analyse application.

"""

import argparse
import os
import sys
import FolderAnalyse
from FolderAnalyse.process import process_dir, process_file


def get_parser():
    parser = argparse.ArgumentParser(
            description="%(prog)s  [options]\n"
                        "Produce word statistics for files in a directory."
                         )

    parser.add_argument('path', type=str,
                        help="path to a directory or a file.")

    parser.add_argument('-t', '--type', type=str, default='txt',
                        help="if path is to a directory, file extension of\n"
                             "files that to be processed.")

    parser.add_argument('-c', '--case', action='store_false',
                        help="by default, processing is not case sensitive.\n"
                             "Add this flag to make it case sensitive")

    parser.add_argument('-N', '--number', type=int, default=10,
                        help="show the top N frequencies for the file(s) and\n"
                             "directory.")

    parser.add_argument('-s', '--save', type=str,
                        help="save the statistics report to the filename.")

    parser.add_argument('-r', '--runtests', action='store_true',
                        help="Ignore all other options and run the tests for"
                             "the module")
    return parser


def exit(message, parser):
    """
    exit(message)

    Quits the running application and gives an error message
    of message.
    """
    parser.print_help()
    print(f"\n\nError: {message}. See above for help.")
    sys.exit()


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.runtests:
        FolderAnalyse.runtests()
        sys.exit()

    path = args.path
    extension = args.type
    case = args.case

    N = args.number

    directory = os.path.isdir(path)
    file = os.path.isfile(path)

    if file:
        stats_text, freq_dict = process_file(path, N, case)

    elif directory:
        try:
            stats_text, freq_dicts, combined_dict = process_dir(path, extension,
                                                                N, case)

        except FileNotFoundError:
            exit(f"No files with extension {extension} found in directory",
                 parser)

    else:
         exit("File or directory does not exist", parser)

    print(stats_text)

    if args.save:
        f = open(args.save, 'w')
        f.write(stats_text)
        f.close()
        print(f"\nSaved report to \"{args.save}.\"")


if __name__ == '__main__':
    main()
