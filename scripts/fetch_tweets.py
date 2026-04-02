#!/usr/bin/env python3
"""
Fetch tweets from accounts defined in config.json.

Usage:
  python fetch_tweets.py              # fetch tweets, output JSON to stdout
  python fetch_tweets.py --count 10   # fetch with custom count per account
  python fetch_tweets.py --days 7     # only include tweets within 7 days
  python fetch_tweets.py --batch-mode # save tweets in batches to .cache/tweets/
  python fetch_tweets.py --batch-mode --batch-size 10 --output-dir .cache/tweets
  python fetch_tweets.py --batch-mode --days 7  # batch mode with time filter
"""
import argparse
import subprocess
import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone


def parse_tweet_date(date_str):
    """Parse tweet date string to datetime object.

    Handles bird CLI format: "Wed Mar 25 10:51:48 +0000 2026"
    Returns None if parsing fails.
    """
    if not date_str:
        return None

    # Bird CLI format: "Wed Mar 25 10:51:48 +0000 2026"
    try:
        return datetime.strptime(date_str.strip(), "%a %b %d %H:%M:%S %z %Y")
    except ValueError:
        return None


def is_within_days(tweet, days):
    """Check if tweet is within the specified number of days.

    Returns True if tweet date is within days, False otherwise.
    """
    if not tweet.get('date'):
        return False

    tweet_date = parse_tweet_date(tweet['date'])
    if not tweet_date:
        return False

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    return tweet_date >= cutoff_date


def load_env():
    """从 .env 文件加载环境变量（向上查找项目根目录）"""
    for parent in [Path(__file__).parent] + list(Path(__file__).resolve().parents):
        env_file = parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            return


load_env()


SKILL_DIR = Path(__file__).resolve().parent.parent


def load_accounts():
    """Load enabled Twitter accounts from config.json.

    Raises FileNotFoundError if config.json is missing.
    Raises ValueError if no enabled accounts are found.
    """
    config_path = SKILL_DIR / 'config.json'
    if not config_path.exists():
        raise FileNotFoundError(
            f"config.json not found at {config_path}. "
            "This file is required -- it defines all Twitter accounts to monitor."
        )
    with open(config_path, 'r') as f:
        config = json.load(f)
    accounts = [a['handle'] for a in config['sources']['twitter_accounts']
                if a.get('enabled', True)]
    if not accounts:
        raise ValueError("No enabled Twitter accounts found in config.json")
    return accounts


def fetch_tweets(account, count=20):
    """Fetch tweets for a single account using bird CLI.

    Returns list of tweet dicts on success, None on error.
    """
    try:
        result = subprocess.run(
            ['bird', 'user-tweets', f'@{account}', '--count', str(count), '--plain'],
            capture_output=True, text=True, timeout=30, env=os.environ.copy()
        )
        if result.returncode != 0:
            return None
        return parse_bird_output(result.stdout, account)
    except Exception as e:
        print(f"Error fetching @{account}: {e}", file=sys.stderr)
        return None


def parse_bird_output(output, account):
    """Parse bird --plain output into structured tweet data.

    Bird --plain format per tweet:
        @handle (Name):
        Tweet text line 1
        Tweet text line 2
        date: Wed Mar 25 10:51:48 +0000 2026
        url: https://x.com/handle/status/123456789
        ──────────────────────────────────────────────────

    Parses by splitting on separator lines, then extracting fields from each block.
    """
    tweets = []
    separator = re.compile(r'^[─━]{5,}')

    blocks = re.split(r'\n[─━]{5,}\n?', output)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        tweet = {'account': account}
        text_lines = []

        for line in block.split('\n'):
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Extract URL and tweet ID
            url_match = re.search(r'https://x\.com/\w+/status/(\d+)', line)
            if url_match:
                tweet['id'] = url_match.group(1)
                tweet['url'] = f"https://x.com/{account}/status/{url_match.group(1)}"
                continue

            # Extract date
            date_match = re.match(r'date:\s*(.+)', line_stripped)
            if date_match:
                tweet['date'] = date_match.group(1)
                continue

            # Skip account header line (e.g. "@handle (Name):")
            if re.match(r'^@\w+\s+\(.+\):', line_stripped):
                continue

            # Remaining lines are tweet text
            text_lines.append(line_stripped)

        if text_lines:
            tweet['text'] = ' '.join(text_lines)

        if 'id' in tweet:
            tweets.append(tweet)

    return tweets


def get_tweets(accounts=None, count=20, days=None):
    """Fetch tweets from all accounts.

    Args:
        days: If set, only include tweets within this many days.

    Returns (tweets, tweet_ids, failed_accounts).
    """
    if accounts is None:
        accounts = load_accounts()

    all_tweets = []
    failed_accounts = []
    filtered_by_date = 0

    for i, account in enumerate(accounts, 1):
        print(f"[{i}/{len(accounts)}] @{account}...", end=" ", file=sys.stderr)
        tweets = fetch_tweets(account, count)
        if tweets is None:
            failed_accounts.append(account)
            print("FAILED", file=sys.stderr)
            continue
        if days is not None:
            before = len(tweets)
            tweets = [t for t in tweets if is_within_days(t, days)]
            filtered_by_date += before - len(tweets)
        if tweets:
            print(f"{len(tweets)} found", file=sys.stderr)
            all_tweets.extend(tweets)
        else:
            print("none", file=sys.stderr)

    if days is not None and filtered_by_date > 0:
        print(f"Filtered out {filtered_by_date} tweets older than {days} days", file=sys.stderr)

    tweet_ids = [t['id'] for t in all_tweets]
    return all_tweets, tweet_ids, failed_accounts


def get_tweets_by_account(accounts=None, count=20, days=None):
    """Fetch tweets grouped by account (for batch processing).

    Args:
        days: If set, only include tweets within this many days.

    Returns dict: {account: [tweets], ...}, tweet_ids, failed_accounts.
    """
    if accounts is None:
        accounts = load_accounts()

    tweets_by_account = {}
    failed_accounts = []
    filtered_by_date = 0

    for i, account in enumerate(accounts, 1):
        print(f"[{i}/{len(accounts)}] @{account}...", end=" ", file=sys.stderr)
        tweets = fetch_tweets(account, count)
        if tweets is None:
            failed_accounts.append(account)
            print("FAILED", file=sys.stderr)
            continue
        if days is not None:
            before = len(tweets)
            tweets = [t for t in tweets if is_within_days(t, days)]
            filtered_by_date += before - len(tweets)
        if tweets:
            print(f"{len(tweets)} found", file=sys.stderr)
            tweets_by_account[account] = tweets
        else:
            print("none", file=sys.stderr)

    if days is not None and filtered_by_date > 0:
        print(f"Filtered out {filtered_by_date} tweets older than {days} days", file=sys.stderr)

    all_tweets = [t for tweets in tweets_by_account.values() for t in tweets]
    tweet_ids = [t['id'] for t in all_tweets]
    return tweets_by_account, tweet_ids, failed_accounts


def save_batches(tweets_by_account, batch_size, output_dir):
    """Save tweets in batches to separate JSON files.

    Args:
        tweets_by_account: dict of {account: [tweets]}
        batch_size: number of accounts per batch
        output_dir: directory to save batch files

    Returns:
        list of batch file paths
    """
    output_path = Path.cwd() / output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    # Clear old batch files
    for old_file in output_path.glob("batch_*.json"):
        old_file.unlink()

    accounts = list(tweets_by_account.keys())
    batch_files = []

    for batch_num, i in enumerate(range(0, len(accounts), batch_size), 1):
        batch_accounts = accounts[i:i+batch_size]
        batch_tweets = []

        for account in batch_accounts:
            batch_tweets.extend(tweets_by_account[account])

        batch_file = output_path / f"batch_{batch_num}.json"
        batch_data = {
            "batch_number": batch_num,
            "accounts": batch_accounts,
            "tweet_count": len(batch_tweets),
            "tweets": batch_tweets
        }

        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)

        batch_files.append(str(batch_file))
        print(f"Saved batch {batch_num}: {len(batch_accounts)} accounts, {len(batch_tweets)} tweets", file=sys.stderr)

    return batch_files


def main():
    parser = argparse.ArgumentParser(
        description='Fetch tweets from config.json accounts')
    parser.add_argument('--count', type=int, default=20,
                        help='Number of tweets to fetch per account (default: 20)')
    parser.add_argument('--batch-mode', action='store_true',
                        help='Save tweets in batches to separate files')
    parser.add_argument('--batch-size', type=int, default=10,
                        help='Number of accounts per batch (default: 10)')
    parser.add_argument('--output-dir', type=str, default='.cache/tweets',
                        help='Directory to save batch files (default: .cache/tweets)')
    parser.add_argument('--days', type=int, default=None,
                        help='Only include tweets within this many days (default: no filter)')
    args = parser.parse_args()

    accounts = load_accounts()

    if args.batch_mode:
        # Batch mode: save to separate files
        tweets_by_account, tweet_ids, failed = get_tweets_by_account(accounts, count=args.count, days=args.days)

        if not tweets_by_account:
            result = {
                "total_accounts": len(accounts),
                "accounts_checked": len(accounts) - len(failed),
                "accounts_failed": [f"@{a}" for a in failed],
                "total_tweets": 0,
                "message": "No tweets found"
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            batch_files = save_batches(tweets_by_account, args.batch_size, args.output_dir)
            result = {
                "total_accounts": len(accounts),
                "accounts_checked": len(accounts) - len(failed),
                "accounts_failed": [f"@{a}" for a in failed],
                "total_tweets": len(tweet_ids),
                "batch_count": len(batch_files),
                "batch_files": batch_files,
                "tweet_ids": tweet_ids
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Standard mode: output to stdout
        tweets, tweet_ids, failed = get_tweets(accounts, count=args.count, days=args.days)
        result = {
            "total_accounts": len(accounts),
            "accounts_checked": len(accounts) - len(failed),
            "accounts_failed": [f"@{a}" for a in failed],
            "tweets": tweets,
            "total_tweets": len(tweets),
            "tweet_ids": tweet_ids
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
