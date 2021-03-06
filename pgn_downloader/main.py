#!/usr/bin/env python3
import argparse

import requests


def cli_arguments(args=None):
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("-o", "--output", default=None, help="Output filename")

    args = parser.parse_args()
    args.output = args.output if args.output is not None else f"{args.username}.pgn"

    return args


def download_pgn(username: str):
    """Downloads games and concatenates to string"""
    print(f"Loading Games for user {username} on chess.com")

    r_archives = requests.get(
        f"https://api.chess.com/pub/player/{username}/games/archives"
    )
    archives = r_archives.json()["archives"]

    pgn = ""
    nr_games = 0
    for month_url in archives:
        print(f"Downloading games from {month_url[-7:]}", end="\r")
        games = requests.get(month_url).json()["games"]
        for game in games:
            try:
                pgn += game["pgn"] + "\n\n"
                nr_games += 1
            except KeyError:
                pass

    print(f"\nDownloaded {nr_games} games")
    return pgn


def cli_entrypoint():
    args = cli_arguments()
    pgn = download_pgn(args.username)

    with open(args.output, "w") as f:
        f.write(pgn)

    print(f"Saved pgn to {args.output}")


if __name__ == "__main__":
    cli_entrypoint()
