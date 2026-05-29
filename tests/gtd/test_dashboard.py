from flow import refresh_dashboard as rd

def _w(tmp_path, name, s):
    p = tmp_path / name
    p.write_text(s, encoding="utf-8")
    return p

def test_count_captures_ignores_headers_comments_separators(tmp_path):
    f = _w(tmp_path, "inbox.md", "# Inbox\n<!-- v1.0.0 -->\n\n> instructions\n---\n")
    assert rd.count_captures(f) == 0

def test_count_captures_counts_real_items(tmp_path):
    f = _w(tmp_path, "inbox.md", "# Inbox\n<!-- c -->\n- call dentist\n- email Sam\nplain idea\n")
    assert rd.count_captures(f) == 3

def test_count_checkboxes_only_counts_tasks(tmp_path):
    f = _w(tmp_path, "na.md",
           "# Next\n<!-- v -->\n## @me\n*(focus)*\n- [ ] task one\n- [ ] task two\n---\n## @claude\n- [ ] task three\n")
    assert rd.count_checkboxes(f) == 3

def test_count_waiting_rows_excludes_header_and_separator(tmp_path):
    f = _w(tmp_path, "wf.md",
           "# Waiting\n| Item | From | Date Sent | Expected By |\n|---|---|---|---|\n<!-- none -->\n")
    assert rd.count_waiting_rows(f) == 0

def test_count_waiting_rows_counts_data_rows(tmp_path):
    f = _w(tmp_path, "wf.md",
           "| Item | From | Date Sent | Expected By |\n|---|---|---|---|\n| reply | Acme | 2026-01-01 | 2026-01-08 |\n")
    assert rd.count_waiting_rows(f) == 1
