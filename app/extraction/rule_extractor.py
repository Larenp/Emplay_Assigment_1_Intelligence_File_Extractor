import re


def extract_emails(text: str) -> list[str]:
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return sorted(set(re.findall(pattern, text)))


def extract_phone_numbers(text: str) -> list[str]:
    pattern = r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}"
    return sorted(set(re.findall(pattern, text)))


def extract_urls(text: str) -> list[str]:
    pattern = r"https?://[^\s]+"
    urls = re.findall(pattern, text)

    # Remove common punctuation accidentally captured at the end.
    return sorted(
        set(url.rstrip(".,;:)") for url in urls)
    )


def extract_dates(text: str) -> list[str]:
    pattern = (
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b"
        r"|\b\d{1,2}-[A-Z]{3}-\d{4}\b"
    )
    return sorted(set(re.findall(pattern, text)))


def extract_rfp_numbers(text: str) -> list[str]:
    pattern = (
        r"(?i)(?:request\s+for\s+proposal|rfp)"
        r"[\s#:.-]*(\d+)"
    )
    return sorted(set(re.findall(pattern, text)))


def extract_amounts(text: str) -> list[str]:
    pattern = r"\$\s?\d+(?:,\d{3})*(?:\.\d{2})?"
    return sorted(set(re.findall(pattern, text)))


def extract_rule_based(text: str) -> dict:
    """
    Extract deterministic information using regular expressions.
    """

    return {
        "emails": extract_emails(text),
        "phone_numbers": extract_phone_numbers(text),
        "urls": extract_urls(text),
        "dates": extract_dates(text),
        "rfp_numbers": extract_rfp_numbers(text),
        "amounts": extract_amounts(text),
    }