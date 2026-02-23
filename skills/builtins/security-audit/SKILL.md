# Security Audit

Audit code and dependencies for security vulnerabilities.

## When to Use
- Before merging PRs
- When reviewing third-party dependencies
- During security review phases
- When user mentions security, vulnerabilities, or audit

## Checklist
1. **Input Validation** — Check all user inputs are sanitized
2. **SQL Injection** — Verify parameterized queries
3. **XSS** — Check output encoding in templates
4. **Auth/AuthZ** — Verify access controls on endpoints
5. **Secrets** — Scan for hardcoded keys, tokens, passwords
6. **Dependencies** — Check for known CVEs in packages
7. **File Access** — Verify path traversal protections
8. **CORS** — Check cross-origin policies
9. **Logging** — Ensure no PII/secrets in logs
10. **Error Handling** — No stack traces in production responses

## Commands
```bash
# Check Python deps
pip audit

# Check npm deps
npm audit

# Scan for secrets
grep -rn "password\|secret\|api_key\|token" --include="*.py" --include="*.js"
```

## Output Format
Report findings as:
- **CRITICAL**: Must fix before merge
- **HIGH**: Fix soon
- **MEDIUM**: Plan to fix
- **LOW**: Nice to fix
- **INFO**: Informational
