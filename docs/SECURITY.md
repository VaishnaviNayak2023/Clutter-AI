# Security

## Local-First Design

The AI Digital Clutter Cleaner is designed as a local-first application:

- All file processing happens on your machine
- No document contents are sent to external services
- No telemetry or analytics by default
- No cloud storage integration

## File Operation Safety

### Path Validation

- All paths are resolved and validated before operations
- Operations restricted to authorized root directories
- Path traversal attacks prevented
- Symlinks not followed by default

### File Move Safety

- Destination conflicts detected before moves
- No silent overwrites
- Source file integrity verified before operation
- Cross-filesystem moves handled safely
- Interrupted operations are recoverable

### No Automatic Deletion

- Files are never deleted automatically
- Exact duplicates are flagged for review only
- User must explicitly approve any file removal
- Undo capability for reversible operations

## Data Privacy

### Document Contents

- Extracted text stored locally in SQLite database
- No document uploads to cloud services
- Sensitive information never leaves your machine
- Database can be deleted at any time

### AI Models

- Embedding models downloaded from Hugging Face on first run
- Models run locally on your machine
- No inference performed on external servers
- Model weights cached locally

## Limitations

### Streamlit Security

- Streamlit binds to a network interface by default
- Application intended for trusted local use
- Do not expose publicly without authentication
- Consider firewall rules for network access

### Input Validation

- Document contents treated as untrusted input
- File size and page count limits enforced
- Extraction time limits prevent resource exhaustion
- Malformed documents handled gracefully

## Best Practices

1. **Test First**: Always test with a copy of your files, not originals
2. **Review Carefully**: Inspect proposals before approving moves
3. **Backup Important Data**: Keep backups of critical documents
4. **Use Exclusions**: Exclude sensitive directories from scans
5. **Check Permissions**: Ensure the application has appropriate filesystem access

## Reporting Security Issues

If you discover a security vulnerability, please:

1. Do not open a public issue
2. Email details to the project maintainer
3. Include steps to reproduce
4. Allow time for investigation and fix

Security issues will be addressed promptly and responsibly.
