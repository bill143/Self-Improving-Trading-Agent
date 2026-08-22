"""Pure HTML rendering for the mission-control dashboard.

Kept dependency-free (no FastAPI import) so it is unit-testable and the web server is
a thin wrapper. Read-only: the dashboard reports state, it never mutates it.
"""

from __future__ import annotations

from html import escape

_CSS = """
:root{--bg:#f6f7f9;--card:#fff;--fg:#111827;--muted:#6b7280;--line:#e5e7eb;
--ok:#137a4b;--okbg:#e7f6ee;--warn:#9a6700;--warnbg:#fff4d6;--bad:#b42318;--badbg:#fdeceb;}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--card:#171a21;
--fg:#e5e7eb;--muted:#9aa4b2;--line:#262b35;--okbg:#0f2a1e;--warnbg:#2a2410;--badbg:#2a1512;}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:24px}
h1{font-size:22px;margin:0 0 2px}.sub{color:var(--muted);margin:0 0 20px}
.banner{padding:16px 20px;border-radius:12px;font-weight:600;margin-bottom:20px}
.banner.ok{background:var(--okbg);color:var(--ok)}.banner.bad{background:var(--badbg);color:var(--bad)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.tile .n{font-size:26px;font-weight:700}.tile .l{color:var(--muted);font-size:13px}
.tile.bad .n{color:var(--bad)}.tile.warn .n{color:var(--warn)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:16px;overflow-x:auto}
.card h2{font-size:15px;margin:0 0 10px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600}.pill{font-size:12px;color:var(--muted)}
.foot{color:var(--muted);font-size:12px;margin-top:8px}
"""


def _rows(items: list[dict]) -> str:
    if not items:
        return '<tr><td colspan="4" class="pill">None</td></tr>'
    out = []
    for it in items:
        out.append(
            f"<tr><td>{escape(str(it.get('name','')))}</td>"
            f"<td class='pill'>{escape(str(it.get('regulator','')))}</td>"
            f"<td>{escape(str(it.get('subject','')))}</td>"
            f"<td>{escape(str(it.get('due_at','')))}</td></tr>")
    return "".join(out)


def render_dashboard(readiness: dict, register_health: dict, policy_status: dict) -> str:
    ready = readiness.get("audit_ready")
    banner = ('<div class="banner ok">✅ Audit-ready — no overdue obligations</div>'
              if ready else
              f'<div class="banner bad">⛔ NOT audit-ready — '
              f'{readiness.get("overdue_count",0)} overdue obligation(s)</div>')

    empty = register_health.get("empty_registers", [])
    tiles = f"""
    <div class="grid">
      <div class="tile {'bad' if readiness.get('overdue_count') else ''}">
        <div class="n">{readiness.get('overdue_count',0)}</div><div class="l">Overdue</div></div>
      <div class="tile {'warn' if readiness.get('due_soon_count') else ''}">
        <div class="n">{readiness.get('due_soon_count',0)}</div><div class="l">Due soon</div></div>
      <div class="tile"><div class="n">{readiness.get('upcoming_count',0)}</div><div class="l">Upcoming</div></div>
      <div class="tile {'warn' if empty else ''}">
        <div class="n">{len(empty)}</div><div class="l">Empty registers</div></div>
      <div class="tile {'warn' if policy_status.get('missing_count') else ''}">
        <div class="n">{policy_status.get('registered_count',0)}/{policy_status.get('required_count',0)}</div>
        <div class="l">Policies registered</div></div>
    </div>"""

    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Everlasting Care — Compliance Mission Control</title><style>{_CSS}</style></head>
<body><div class="wrap">
<h1>Everlasting Care — Compliance Mission Control</h1>
<p class="sub">NDIS Certification pathway · Sydney · read-only · generated {escape(str(readiness.get('generated_at','')))}</p>
{banner}
{tiles}
<div class="card"><h2>Overdue obligations</h2><table>
<tr><th>Obligation</th><th>Regulator</th><th>Subject</th><th>Was due</th></tr>
{_rows(readiness.get('overdue', []))}</table></div>
<div class="card"><h2>Due soon</h2><table>
<tr><th>Obligation</th><th>Regulator</th><th>Subject</th><th>Due</th></tr>
{_rows(readiness.get('due_soon', []))}</table></div>
<div class="card"><h2>Policy suite</h2>
<p class="pill">{policy_status.get('registered_count',0)} of {policy_status.get('required_count',0)} required policies registered ·
{policy_status.get('missing_count',0)} missing · {len(policy_status.get('overdue_review', []))} overdue for review</p></div>
<div class="card"><h2>Registers</h2>
<p class="pill">{register_health.get('registers',0)} registers · {"all populated" if register_health.get('all_populated') else escape(', '.join(empty)) + " empty"}</p></div>
<p class="foot">This dashboard assists compliance oversight. It does not replace the qualified human sign-off required before real audits or claims.</p>
</div></body></html>"""
