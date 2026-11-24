# Wildcard scope pipeline

Use this only after the program authorization and a scope file exist. The
script `scripts/wildcard-recon.sh` owns budgets, rate limits, and the scope
filter. Do not raise those limits from a prompt.

## Scope rules

- `*.example.com` allows only names under that suffix. The apex is not in scope
  unless the scope file also lists `example.com`.
- `.example.com` allows the apex and every name under it. This is the suffix
  form already used by `automation/authorized-recon.sh`.
- An exact host allows only that host.
- The seed `--domain` must be the suffix of one wildcard line in the scope file.
- Every host and URL is filtered again before a live check reads it.

## Stages

1. Passive names: `subfinder`, `assetfinder`, `amass` passive, `findomain`,
   `uncover`, certificate transparency. `github-subdomains` runs only when
   `GITHUB_TOKEN` or `GH_TOKEN` is already set.
2. Passive URLs: `gau`, `waybackurls`, `urlfinder`, `waymore`, `paramspider`.
   `uro` dedupes the in-scope list. `unfurl` extracts paths and parameter
   names locally.
3. Active, only with `--i-am-authorized`: at most 500 `alterx` names from the
   first 100 in-scope hosts, then `dnsx`, `tlsx`, `cdncheck`, `httpx`, bounded
   `katana` and `hakrawler`, `wafw00f` and `whatweb` on the host budget,
   bounded `ffuf`, bounded `arjun`, and non-intrusive `nuclei`.
4. `naabu` top-ports only when `--enable-port-scan` is also present.

`asnmap` and `mapcidr` stay installed for a manual range question. The script
does not run them, because a range can leave the wildcard. `puredns` is the
same: `dnsx` already resolves the filtered names. `qsreplace` is not run,
because it rewrites URLs into request payloads.

Missing binaries are recorded in `meta/missing-tools.txt` and skipped. The
script does not install tools. Installation does not authorize traffic.

## Output

Inventory files live under the chosen `--out` directory:

- `passive/subdomains-in-scope.txt`
- `passive/historical-urls-in-scope.txt`
- `passive/param-names.txt`
- `active/live-urls-in-scope.txt`
- `active/fingerprint.txt`
- `active/katana-urls-in-scope.txt`
- `active/paramspider-urls-in-scope.txt`
- `active/ffuf-hits.txt`
- `active/arjun/`
- `active/nuclei-non-intrusive.txt`
- `summary.txt`

`summary.txt` is a count sheet. It is not a vulnerability list. A live host,
a path, a parameter, or a nuclei line stays `HYPOTHESIS_QUARANTINED` until a
later validation skill proves a security boundary failure on an in-scope asset.

## Stop

Stop when the program forbids automation, the scope line is not a wildcard,
a response is 429, the application looks unstable, or a result belongs to
another customer or a third-party host. Do not evade a block, rotate
addresses, or follow redirects outside the scope file.
