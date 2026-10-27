# demo_showcase

Presents the installed MultiFlexi applications on a public demo instance in a believable way and keeps the
instance maintainable while it is deliberately open to anonymous experiments.

The demo is meant to be poked at: whatever visitors manage to do is **observed first, cleaned afterwards**.
Applications themselves come from the installed `multiflexi-*` packages (role `demo`); this role presents them
and guards the instance. It talks to MultiFlexi only through `multiflexi-cli` (modules of this collection).

Requires MySQL/MariaDB for `snapshot`/`reset` (the dump is taken with `mysqldump` over the local socket).

## Modes (`demo_showcase_mode`)

| Mode | What it does | Typical schedule |
|---|---|---|
| `seed` | installs `debsums`, creates fictional companies, assigns applications to them, creates run templates, then runs `snapshot` | after every (re)deployment |
| `snapshot` | records the baseline: allowlist of records, sha256 manifest of watched files, listening TCP ports, database dump + checksum | after `seed`, after intended changes |
| `reconcile` | archives, then removes records outside the allowlist (event rules/sources, tokens, credentials, applications, users), re-asserts the showcase | every 15 min |
| `audit` | read-only: classifies the instance as `clean` / `data_abuse` / `host_compromise`, writes a report, runs `incident` and **fails** on `host_compromise` | every 5 min |
| `reset` | verifies the dump checksum, stops workers + web, restores the baseline DB, restarts, smoke-tests, audits | daily (night) |
| `incident` | containment + evidence (see below); never restores or restarts anything | automatic from `audit`, or manual |

All modes are idempotent and can be repeated.

## Observing what visitors do

`reconcile` writes every record it is about to remove, **in full** (e.g. the `executable` of an application created by a
visitor), to `{{ demo_showcase_state_dir }}/observed/<time>-reconcile.json` (mode 0600, kept
`demo_showcase_observed_retention_days` days) and logs a summary to the journal under the identifier `demo-guard`
(the OTEL journald receiver ships it to Loki). `audit` logs its result the same way (`auth.info` clean, `auth.warning`
data abuse, `auth.alert` host compromise), so alerts can be built on priority.

Secret fields (passwords, tokens, API keys) are masked as `***` by the `*_info` modules, so neither the archive nor
the journal ever holds them. Visitor-controlled values are only handled by filters that keep Ansible's untrusted
marking (no `to_json`/`from_json` round trips), so a hostile record name such as `{{ lookup('pipe', ...) }}` stays
inert text.

Set `demo_showcase_reconcile_dry_run: true` to only observe: records are archived and reported but not deleted.
Use it only on an isolated host, since a visitor-created application can execute code.

## Detection

Data level (`reconcile` entities): anything not in the baseline allowlist.
Host level (`audit`): changed packaged files (`debsums`, restricted to `demo_showcase_debsums_globs`), changed
files under `demo_showcase_watch_paths`, **new** listening TCP ports, executables in `demo_showcase_scratch_dirs`.
After a legitimate change of watched files (e.g. a package upgrade rewriting `/etc/multiflexi/multiflexi.env`) run
`snapshot` again, otherwise `audit` reports it.

## Incident

`incident` stops the workers (and the web service), saves evidence to
`{{ demo_showcase_backup_dir }}/incident-<time>/` (processes, sockets, journal, logins, cron, scratch dirs, recently
changed files, forensic DB dump, audit report), logs at `auth.alert` and optionally mails
`demo_showcase_notify_mail_to`. The host must then be rebuilt from a clean image and redeployed; rotate the secrets
that lived on it. Containment of the network (egress firewall, separate segment) is outside this role and is the
actual protection against an executed payload - the role only limits how long and how visibly it can persist.

## Not covered

* Job history is not seeded; run templates are created inactive (`demo_showcase_runtemplates_active`).
* `reset` restores the database only. Files visitors may have written elsewhere are found by `audit`, not removed.
* SQLite/PostgreSQL backends for `snapshot`/`reset`.
* The `interv` codes in `demo_showcase_intervals` follow the run template interval codes of the CLI; check them on a real instance.

## Example

```yaml
- hosts: demo.multiflexi.eu
  become: true
  roles:
    - role: vitexus.multiflexi.demo_showcase
      vars:
        demo_showcase_mode: reconcile
```

Keep `demo_showcase_expected_dump_sha256` (printed by `snapshot`) outside the host, e.g. in the Semaphore
environment, so `reset` refuses a tampered dump.
