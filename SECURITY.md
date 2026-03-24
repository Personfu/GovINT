# Security Policy

## Scope

This project is a static website served via GitHub Pages. It has no backend, no database, no authentication, and collects no user data.

The attack surface is limited to:

- **Cross-site scripting (XSS)** via injected content in upstream government data feeds
- **Subresource integrity** of third-party CDN resources (Leaflet.js)
- **Link injection** via malformed URLs in feed data

## Reporting a Vulnerability

If you discover a security issue, please report it responsibly:

1. **Do not** open a public issue
2. Email: open a [GitHub Security Advisory](https://github.com/Personfu/GovINT/security/advisories/new) (preferred)
3. Include: description, reproduction steps, and potential impact

We aim to acknowledge reports within 48 hours and resolve confirmed vulnerabilities within 7 days.

## Mitigations in Place

- All feed data is HTML-entity-escaped before DOM insertion (`esc()` in `feed-loader.js`)
- URLs from feed data are validated against `https?://` or `/` prefix before rendering
- External links use `target="_blank" rel="noopener"` to prevent reverse tabnapping
- No `eval()`, `document.write()`, or inline event handlers
- No cookies, localStorage tokens, or session state
- No user input forms or file uploads

## Out of Scope

- Content accuracy of upstream government data feeds
- Availability of third-party APIs (CISA, FBI, DHS, etc.)
- Security of linked external government websites
