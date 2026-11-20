# Expert Programming Language Matrix

Use this matrix to select skills by actual runtime boundaries, not file extension alone.

| Runtime / surface | Primary skill | Mandatory cross-checks |
|---|---|---|
| Python service, CLI, data tool | `expert-python-engineer` | packaging, async cancellation, runtime validation, subprocess/file boundaries |
| Browser, Node.js, TypeScript full stack | `expert-javascript-typescript-engineer` | runtime schemas, ESM/CJS, prototype/object semantics, browser/server trust |
| Go service/controller/CLI | `expert-go-engineer` | goroutine ownership, context, build tags, race detector, module provenance |
| Rust systems/service/WASM | `expert-rust-engineer` | unsafe/FFI contracts, feature matrix, async cancellation, Cargo build scripts |
| Native C/C++ or Windows/Linux systems | `expert-c-cpp-engineer` | ABI, ownership, UB, concurrency, platform APIs, release flags |
| JVM/Android Java/Kotlin | `expert-java-kotlin-engineer` | serializer/classloader, framework filters, coroutines, final JAR/APK artifacts |
| .NET/Windows service/ASP.NET | `expert-dotnet-csharp-engineer` | middleware/claims, async lifetime, serializer, PInvoke, publish/trimming |
| PHP/Ruby dynamic web apps | `expert-php-ruby-engineer` | policy/model/job flow, coercion, metaprogramming, plugin/package trust |
| Bash/POSIX/PowerShell automation | `expert-shell-powershell-engineer` | quoting, argument arrays, environment, idempotency, cleanup, secret exposure |
| SQL/schema/migrations | `expert-sql-database-engineer` | business invariants, isolation, RLS/roles, old/new app compatibility, recovery |
| Binary-only, stripped, patch diff | `expert-reverse-engineer` | exact hashes, symbol provenance, static + dynamic confirmation |
| Windows service/driver/Defender/WinRE | `expert-windows-internals-vulnerability-researcher` | build/KB, token/object identity, links/oplocks/races, vendor patch status |

## Polyglot rule

Real systems cross languages. Trace serialization, error, identity, tenant, signature, path, time, number, and concurrency semantics across each boundary. A check in one language is not proof that another runtime interprets the value identically.
