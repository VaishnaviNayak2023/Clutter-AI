# User Guide

## Getting Started

### Launching the Application

1. Open a terminal or command prompt
2. Navigate to the project directory
3. Activate your virtual environment
4. Run: `streamlit run app.py`
5. The application will open in your browser at `http://localhost:8501`

Page navigation is reflected in the `view` query parameter, so a page can be opened
directly (for example, `http://localhost:8501/?view=Search_Explorer`) and browser
back/forward navigation follows page changes.

### First-Time Setup

On first launch, the application will:
- Initialize the SQLite database
- Create necessary tables
- Download embedding models (when AI features are used)

## Pages Overview

### Overview

The Overview dashboard uses files scanned in the current Streamlit session. It shows
file count, storage, hash-based duplicate groups, completed organization moves,
category and extension charts, AI insights, and recent session activity. Empty
workspaces retain the dashboard layout and offer a path to start a scan.

### Scan Files

Scan a directory to analyze supported files:

1. Enter a folder path accessible to the machine running ClutterAI
   (for example, `C:\Users\YourName\Downloads`).
2. Choose whether to scan subdirectories, calculate SHA-256 hashes, save metadata
   to SQLite, and run text extraction during the scan.
3. Optionally enter path fragments to exclude, one per line.
4. Click **Start scan** and review the resulting file table.

**Tips:**
- Start with a small test folder first
- Use absolute paths for reliability
- Check the scan results before proceeding
- Browser-only deployments cannot browse arbitrary paths on the user's device; use
  a path available to the application host.
- Supported formats are PDF, TXT, Markdown, DOCX, CSV, JSON, and Python files.

### AI Organization

Classification results can be generated explicitly and reviewed before any move:

1. Click **Classify files**.
2. Review predicted categories, confidence, and reasons.
3. Review a file's prediction or adjust its category and inspect proposed destinations.
4. Keep **Dry Run** enabled to validate selected moves without changing files.
5. To execute moves, turn Dry Run off, review the destination list, and explicitly
   confirm before choosing **Execute Organization**.

Completed moves can be undone from this page during the current session if the
destination still exists and the original path is unoccupied. Action history and
undo state are not persisted across restarts.

### Duplicate Finder

Review exact duplicates and semantically similar documents separately:

1. Exact groups are based on identical SHA-256 hashes and require hashing during scan.
2. Semantic analysis extracts document text and compares embeddings. The selected
   similarity threshold filters the computed results. The first run may download
   the configured model.
3. Compare paths and sizes before deciding what to do.

Semantic similarity does not mean that files are byte-identical. The application
does not automatically delete files.

### Search Explorer

Search files from the current scan by name, path, or optionally extracted content:

1. Enter a filename, path fragment, or content query.
2. Filter by extension, category, size, modified date, exact match, and hidden/system
   files.
3. Select a result to inspect its preview, metadata, path, and related files. **Open
   File** downloads a copy through the browser rather than launching a local app.

Content search reads supported files during the search and may take longer on large
scans.

### History & Activity

View activity recorded since the current application session started, including scans,
classification, similarity analysis, organization, and report generation.

The existing history service does not yet persist action events, so this page does not
show events from previous sessions. Undo is available only on the AI Organization page
for eligible moves completed during the current session.

### Reports

Generate a scan summary, category breakdown, duplicate statistics, or storage-by-
extension report. Export reports as CSV or plain text. Category reports require
classification results in the current session.

### Settings

Configure settings stored in the local SQLite database:

1. Set scan defaults for hashes, metadata persistence, and text extraction.
2. Set default excluded path fragments.
3. Adjust the semantic similarity threshold.

## Best Practices

### Before Scanning

1. **Backup Important Files**: Always keep backups of critical documents
2. **Start Small**: Test with a small folder first
3. **Check Permissions**: Ensure the application can access the folder
4. **Review Exclusions**: Exclude sensitive or system directories

### During Organization

1. **Review Carefully**: Don't approve all suggestions blindly
2. **Check Confidence**: Pay attention to low-confidence predictions
3. **Verify Destinations**: Ensure destination paths make sense
4. **Use Dry-Run**: Preview changes before executing

### After Organization

1. **Verify Results**: Check that files are in expected locations
2. **Review Activity**: Confirm operations completed successfully in History & Activity
3. **Undo if Needed**: Use the AI Organization page during the same session
4. **Keep Backups**: The application does not provide persistent undo history

## Troubleshooting

### Scan Fails

- Check that the folder path is correct
- Ensure you have read permissions
- Verify the folder exists
- Check for hidden or system files

### Application Won't Start

- Ensure virtual environment is activated
- Verify dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.11+ required)
- Look for error messages in the terminal

### Database Errors

- Delete the database file (`clutter_cleaner.db`) to reset
- Ensure write permissions in the project directory
- Check disk space availability

### Model Download Fails

- Ensure internet connection for first-time download
- Check firewall settings
- Verify Hugging Face is accessible
- Models will be cached locally after download

## FAQ

**Q: Will the application delete my files?**
A: No. The application never deletes files automatically. You must explicitly approve any file operations.

**Q: Can I undo file moves?**
A: Eligible moves can be undone from AI Organization during the current session.

**Q: Does this work with cloud storage?**
A: The application is designed for local filesystems. Cloud-synced folders may have limitations.

**Q: How accurate is the AI classification?**
A: Accuracy depends on document content and training data. Review suggestions before approving.

**Q: Can I use this on a Mac or Linux?**
A: Yes, the application is cross-platform. Installation steps vary slightly by OS.

**Q: What happens if I interrupt a scan?**
A: Only completed scan results are added to the current session. Start the scan again
to collect a complete result set.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
