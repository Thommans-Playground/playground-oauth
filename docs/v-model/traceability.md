# Traceability Matrix

| Requirement | Use Case | Acceptance Test | Contract/Integration Test | Unit Test(s) |
|---|---|---|---|---|
| FR-01 | UC-01 Register with Password | planned | planned | planned |
| FR-02 | UC-02 Log In with Password | planned | planned | planned |
| FR-03 | UC-03 Log In with OAuth Provider | planned | planned | planned |
| FR-04 | UC-03 Log In with OAuth Provider (account linking) | planned | planned | planned |
| FR-05 | (planned) | — | — | — |
| FR-06 | (planned) | — | — | — |
| FR-07 | UC-02, UC-03 (session creation) | planned | planned | planned |
| FR-08 | UC-04 Log Out | planned | planned | planned |
| FR-09 | (planned) | — | — | — |
| FR-10 | (planned) | — | — | — |
| NFR-01 | — (checked by code review / import-linter, not a use case) | — | planned | — |
| NFR-02 | UC-01, UC-02, UC-03 (password hashing) | — | planned | planned |
| NFR-03 | UC-03 (state + PKCE) | — | planned | — |
| NFR-04 | UC-02, UC-03, UC-04 (cookie flags) | — | planned | — |
| NFR-05 | this file | — | — | — |
| NFR-06 | — | — | planned | — |

This table is updated whenever a use case moves from documented to implemented: fill in
the real test file paths in place of `planned`.
