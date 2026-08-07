# RLEAPP

Returns, Records and Reports parser. Unlike the device extractors, RLEAPP parses the
**returns that providers hand over in response to legal process**: Google, Meta, Snap,
Discord and similar, not an image pulled from a phone.

## What that changes

- **The input is a provider export, not a filesystem.** Structure is whatever the provider
  chose: HTML bundles, CSV, JSON, TXT, sometimes a nested zip. It varies by provider and by
  the date the return was produced, so patterns and parsers age with the provider's format.
- **There is no device.** Do not reach for device-info conventions or assume a path layout.
- **Format changes arrive without warning.** When a return no longer parses, the provider
  changed the export, not the evidence. Add support for the new shape and keep the old one
  working; examiners hold returns going back years.

## Before changing an artifact

This repo does not carry the module-authoring docs. **iLEAPP's
[`admin/docs/artifact_info_block.md`](https://github.com/abrignoni/iLEAPP/blob/main/admin/docs/artifact_info_block.md)
is the reference for the `__artifacts_v2__` block** and applies here unchanged: same
loader, same seekers, same glob semantics.

Some modules build their `__artifacts_v2__` dict through a helper rather than declaring it
literally. Those are invisible to the CI checkers, which `ast.literal_eval` the block, so
they are silently unchecked. Prefer a literal dict in new modules.

## Repo-specific things worth knowing

- `scripts/parse3.py` is a self-contained protobuf decoder. This repo does not depend on
  protobuf or blackboxprotobuf, and should not start.
- Returns routinely contain real personal data for real people. See
  `.claude/rules/leapp-claims.md`, and never put values from a return into a commit
  message, a PR body or a test fixture.

## Rules

`.claude/rules/` holds the detail. Files prefixed `leapp-` are shared across all five
extractors and `lava-` across all six repos. **Edit those at their canonical source, not
here**, or the next sync overwrites you.
