# Commit Message Generator

Generate clear, conventional commit messages from staged git changes.

## When to Use
- When committing code changes
- When preparing release notes
- When reviewing staged diffs

## Instructions
1. Run `git diff --cached` to see staged changes
2. Analyze the nature of changes (feat, fix, refactor, docs, test, chore)
3. Write a concise subject line (max 72 chars) in imperative mood
4. Add body with bullet points explaining "why" not "what"
5. Include breaking change footer if applicable

## Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types
- **feat**: New feature
- **fix**: Bug fix
- **refactor**: Code restructuring (no behavior change)
- **docs**: Documentation only
- **test**: Adding/updating tests
- **chore**: Build, tooling, dependency changes
