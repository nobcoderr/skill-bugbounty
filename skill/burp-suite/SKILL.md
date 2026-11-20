---
name: burp-suite
description: "Use the local Burp Suite proxy and PortSwigger MCP server during authorized web testing. Start Burp when a task needs interception, Repeater, or proxy history, and connect it through the burp MCP server without asking first."
---

# Burp Suite

Burp Suite Community `2026.10.1` is installed at `/usr/bin/burpsuite`.
The PortSwigger MCP Server extension `1.4.0` is installed at
`/home/kali/.local/share/burp/burp-mcp-all.jar`.

- Proxy listener: `127.0.0.1:8080`
- MCP server: `http://127.0.0.1:9876/mcp`
- Start script: `burp-mcp-start`
- Log: `/home/kali/.config/burp/logs/burp.log`

Codex connects directly through Streamable HTTP. The official
`burp-suite-mcp-server@portswigger` plugin supplies the detailed `burp-mcp`
tool guidance. The MCP server name is `burp`.

## When to use it

For an authorized web or API test, start Burp and use the `burp` MCP tools
when the task needs a proxy, Repeater, history, or encoded request editing.
Do not ask whether Burp should be used. Do not set a system-wide proxy.
Point only the testing client at `127.0.0.1:8080`.

If port `9876` is closed, run `burp-mcp-start` and wait until the log says
the MCP server started.

## Limits

Send or replay traffic only to a host already named in the authorized scope.
Do not approve a Burp target outside that scope. Leave Collaborator and
active scanning unused unless the current program allows that exact action.
Intercept stays off unless the task needs to hold one specific request.
