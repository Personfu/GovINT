# Contributing to PERSONFU // Arizona Public Intel Wiki

Thank you for your interest in contributing.

## Ways to Contribute

- **Data corrections** — Fix inaccurate dates, locations, or facts in wiki JSON files
- **New dossier pages** — Write deep-dive content pages for Arizona topics
- **Timeline entries** — Add documented events with sources and reliability ratings
- **Bug fixes** — Fix rendering issues, broken links, or script errors
- **Accessibility** — Improve screen reader support, contrast, keyboard navigation

## Guidelines

### Content Standards

1. **Cite your sources.** Every factual claim needs a source. Government primary sources preferred.
2. **Use the reliability scale.** Rate claims honestly — `verified` means a .gov URL confirms it. Don't inflate.
3. **No speculation presented as fact.** Label speculative content clearly with appropriate reliability badges.
4. **Arizona focus.** Content should have a clear connection to Arizona government, defense, infrastructure, or documented history.

### Code Standards

- Vanilla JavaScript only — no frameworks, no build tools, no npm
- CSS in a single theme file (`assets/css/fllc-govint.css`)
- HTML pages follow the existing header/nav/footer template
- Python scripts should handle errors gracefully and write to `data/latest/`

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/topic-name`)
3. Make your changes
4. Test locally (`python -m http.server 8000`)
5. Submit a PR with a clear description of what changed and why

### Commit Messages

Use conventional format:
```
feat: add Luke AFB dossier page
fix: correct Davis-Monthan aircraft count
data: update timeline with 2024 water ruling
docs: clarify reliability scale definitions
```

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold respectful, constructive interaction.
