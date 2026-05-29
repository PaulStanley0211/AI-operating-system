import pytest
from actions.triage.prefilter import prefilter

@pytest.mark.parametrize("sender,subject,expected", [
    ("noreply@github.com", "Your PR was merged", "ignore"),
    ("no-reply@accounts.google.com", "Security alert", "ignore"),
    ("lbbw-jobnotification@noreply12.jobs2web.com", "Neue Stellen", "ignore"),
    ("hello@students.udemy.com", "Your weekly digest", "ignore"),
    ("billing@stripe.com", "Your receipt from Acme", "ignore"),
    ("Emma Jacobs <emma@stepstone.de>", "Re: AI Engineer role", "candidate"),
    ("Paulina <paulina@eraneos.com>", "Following up on your application", "candidate"),
    ("jane@somestartup.io", "Question about a pilot project", "candidate"),
])
def test_prefilter(sender, subject, expected):
    assert prefilter(sender, subject) == expected
