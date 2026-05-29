import base64
from actions.triage import gmail_draft

def test_build_reply_mime_adds_re_prefix():
    msg = gmail_draft.build_reply_mime("a@b.com", "Interview times", "Sounds good.\nPaul")
    assert msg["Subject"] == "Re: Interview times"
    assert msg["To"] == "a@b.com"
    assert "Sounds good." in msg.get_content()

def test_build_reply_mime_keeps_existing_re():
    msg = gmail_draft.build_reply_mime("a@b.com", "Re: Interview times", "ok")
    assert msg["Subject"] == "Re: Interview times"

def test_build_reply_mime_sets_threading_headers():
    msg = gmail_draft.build_reply_mime("a@b.com", "Hi", "ok", in_reply_to="<abc@mail>")
    assert msg["In-Reply-To"] == "<abc@mail>"
    assert msg["References"] == "<abc@mail>"

def test_create_reply_draft_calls_api_with_thread_and_raw():
    calls = {}
    class FakeDrafts:
        def create(self, userId, body):
            calls["userId"] = userId; calls["body"] = body
            class E:  # noqa
                def execute(self_inner):
                    return {"id": "draft123"}
            return E()
    class FakeUsers:
        def drafts(self): return FakeDrafts()
    class FakeService:
        def users(self): return FakeUsers()

    draft_id = gmail_draft.create_reply_draft(
        FakeService(), thread_id="T1", to="a@b.com", subject="Hi",
        body="ok", in_reply_to="<abc@mail>")
    assert draft_id == "draft123"
    assert calls["body"]["message"]["threadId"] == "T1"
    raw = calls["body"]["message"]["raw"]
    decoded = base64.urlsafe_b64decode(raw).decode()
    assert "To: a@b.com" in decoded
    assert "Re: Hi" in decoded
