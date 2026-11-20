# Authorized Executable Audit Playbook

Use this playbook only for a product you own, an internal engagement, or a bug-bounty target that permits executable/client testing.

## 1. Preserve the target

Record product, platform, architecture, channel, version, artifact hash, signature/notarization identity, download source, installation options, and default configuration. Keep the original package and a clean VM snapshot.

## 2. Map the runtime

Document process tree, user/service identity, integrity/sandbox level, helpers, services, listeners, IPC endpoints, plugins, update agents, scheduled tasks, file associations, custom protocols, and writable directories.

## 3. Map inputs

- network/update responses;
- local files/documents/archives/projects;
- URI/deep links and file associations;
- command line, environment, current directory, PATH, temp/cache/config;
- IPC/native messaging/local listeners;
- plugins/packages/scripts;
- renderer or WebView content;
- parser lengths, offsets, counts, types, compression/container metadata.

## 4. Map sinks

- process/shell/interpreter execution;
- library/plugin/script loading;
- privileged file operations;
- installer/updater replacement and restart;
- deserialize/eval/template callbacks;
- privileged IPC actions;
- native memory copy/index/allocation/free;
- secret/key/token/certificate access.

## 5. Trace both directions

Forward from each controllable input and backward from each critical sink. Record every normalization, validation, authorization, signature, identity, and privilege transition. Do not assume a wrapper is safe or unsafe—inspect it.

## 6. High-yield comparisons

- stable vs beta/debug;
- source vs packaged artifact;
- Windows vs macOS vs Linux implementations;
- normal vs retry/fallback/repair/rollback/uninstall;
- signed metadata vs installed bytes;
- one IPC method vs sibling methods;
- one parser/importer vs legacy/compatibility parser;
- safe call sites vs missing-check call sites.

## 7. Safe verification

Use benign canaries, loopback services, controlled plugins, mock update endpoints, sanitizer/debugger evidence, and temporary researcher-owned files. Include a negative control and document cleanup. Do not use reverse shells, persistence, credentials, destructive operations, or public malicious distribution.

## 8. Candidate validity gate

A candidate is not valid until scope, exact release, realistic attacker capability, full call chain, missing invariant, primitive, boundary, concrete impact, prior-art status, and safe reproduction are documented.
