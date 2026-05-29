"""Deterministic noise pre-filter. The nuanced ignore/draft/gray-zone
decision is made by the model in the /triage skill; this only drops
obvious machine noise so the model reviews fewer items."""

NOISE_SENDER_FRAGMENTS = (
    "noreply@", "no-reply@", "donotreply@", "do-not-reply@",
    "notifications@", "notification@", "mailer@", "mailer-daemon@",
    "bounce@", "bounces@", "noreply12.", "jobnotification@",
)

NOISE_SUBJECT_FRAGMENTS = (
    "unsubscribe", "newsletter", "digest", "weekly roundup",
    "your receipt", "receipt from", "invoice #", "order confirmation",
    "security alert", "verify your email",
)


def prefilter(sender: str, subject: str) -> str:
    """Return "ignore" for obvious machine noise, else "candidate"."""
    s = (sender or "").lower()
    sub = (subject or "").lower()
    if any(frag in s for frag in NOISE_SENDER_FRAGMENTS):
        return "ignore"
    if any(frag in sub for frag in NOISE_SUBJECT_FRAGMENTS):
        return "ignore"
    return "candidate"
