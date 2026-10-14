# Survey 2 — coder A partial labels

Coder A (Claude, AI-assisted) labels saved one information type at a time, so that work survives a
scratchpad wipe. Each `<category>.json` is a list of rows; `server_id` matches `../screening.csv`
(decision `include`). Repos were shallow-fetched at the pinned `commit_sha` and read statically;
no repository code was executed.

Columns follow `../../tool_survey/coding.csv` plus two origin-level columns (protocol §5):

- `origin_a` / `origin_a_evidence` — data origin of the default provider(s), filled **only** when the
  repo itself (code, config, README, description) states it; blank means no repo evidence.

Repo-independent fields (`category`, `repo_url`, `commit_sha`, `coder`) are added when the partial
files are merged into `../coding.csv`. Coder A did not open any human-coder labels.
