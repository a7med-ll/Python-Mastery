def word_count(text: str) -> int:
    """Count the number of words in a string."""
    return len(text.split())


def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome, ignoring case and spaces."""
    cleaned = "".join(text.lower().split())
    return cleaned == cleaned[::-1]


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: textkit <text>")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    print(f"Word count: {word_count(text)}")
    print(f"Is palindrome: {is_palindrome(text)}")


if __name__ == "__main__":
    main()