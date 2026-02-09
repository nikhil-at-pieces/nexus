"""
Build X/Twitter search query for twscrape.
Used by CLI and platform_connectors/x for keyword listening.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Optional


def build_x_search_query(
    keywords: List[str],
    *,
    hours_back: int,
    match_mode: Literal["ALL", "ANY"] = "ANY",
    lang: Optional[str] = None,
    exclude_retweets: bool = True,
) -> str:
    """Build a search query for twscrape from keywords and options."""
    safe_terms = [t.strip() for t in keywords if t and t.strip()]
    if not safe_terms:
        raise ValueError("At least one non-empty keyword is required")

    if match_mode.upper() == "ALL":
        query = " ".join(safe_terms)
    else:
        query = " OR ".join(safe_terms)

    parts: List[str] = [query]
    since = (datetime.now(timezone.utc) - timedelta(hours=hours_back)).strftime("%Y-%m-%d_%H:%M:%S_UTC")
    parts.append(f"since:{since}")
    if lang:
        parts.append(f"lang:{lang}")
    if exclude_retweets:
        parts.append("-filter:nativeretweets")
    return " ".join(parts)


def tweet_to_dict(t: Any) -> Dict[str, Any]:
    """Convert a twscrape tweet object to a plain dict for JSON/output."""
    user = getattr(t, "user", None)
    username = getattr(user, "username", None) if user else None
    displayname = getattr(user, "displayname", None) if user else None
    tweet_id = getattr(t, "id", None)
    url = getattr(t, "url", None)
    if not url and username and tweet_id:
        url = f"https://x.com/{username}/status/{tweet_id}"
    dt = getattr(t, "date", None)
    if hasattr(dt, "astimezone"):
        dt_iso = dt.astimezone(timezone.utc).isoformat()
    else:
        dt_iso = str(dt) if dt is not None else None
    return {
        "id": str(tweet_id) if tweet_id is not None else None,
        "date": dt_iso,
        "username": username,
        "displayname": displayname,
        "text": getattr(t, "rawContent", None),
        "url": url,
        "likes": getattr(t, "likeCount", None),
        "replies": getattr(t, "replyCount", None),
        "retweets": getattr(t, "retweetCount", None),
        "quotes": getattr(t, "quoteCount", None),
    }
