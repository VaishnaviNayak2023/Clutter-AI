# AI Digital Clutter Cleaner

An AI-powered local-first document organizer that scans folders, extracts document contents, categorizes files, detects exact duplicates, discovers semantically similar documents, recommends a clean folder structure, and performs approved, reversible file operations.

## Project Overview

The AI Digital Clutter Cleaner addresses the common problem of cluttered digital workspaces where Downloads and Documents folders contain hundreds of unorganized files with unclear names, duplicate files wasting disk space, and documents that contain nearly identical information despite having different filenames.

The solution: Users select a folder, the application analyzes supported files, and an AI pipeline recommends categories, identifies duplicates, and suggests a cleaner folder structure—all while keeping the user in control of every file operation.

## Key Features

### Currently Implemented (All Phases Complete ✅)

- ✅ **Folder Scanning**: Recursively scan directories and collect file metadata
- ✅ **Document Extraction**: Extract text from TXT, Markdown, CSV, JSON, Python, PDF, and DOCX files
- ✅ **Exact Duplicate Detection**: Identify byte-identical files using SHA-256 hashing
- ✅ **Semantic Similarity**: Discover semantically similar documents using AI embeddings
- ✅ **AI Classification**: Categorize documents using machine learning (scikit-learn)
- ✅ **Database Persistence**: Store scan results in SQLite for future reference
- ✅ **Progress Tracking**: Real-time progress updates during scans
- ✅ **File Type Filtering**: Include/exclude specific file types
- ✅ **Path Exclusions**: Exclude specific directories from scans
- ✅ **Dashboard**: Overview of scan results and statistics
- ✅ **Safe Organization**: Preview and execute file moves with validation
- ✅ **Undo Functionality**: Reversible file operations
- ✅ **Search and Explore**: Advanced file search with filters
- ✅ **Action History**: Track scan, classification, and organization history
- ✅ **Report Generation**: Generate text and CSV reports of scan results
- ✅ **Settings Configuration**: Configure application preferences

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **Machine Learning**: scikit-learn, Sentence Transformers
- **Document Extraction**: pypdf, python-docx
- **Database**: SQLite
- **Testing**: pytest
- **Linting**: ruff

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-digital-clutter-cleaner.git
cd ai-digital-clutter-cleaner
```

2. Create a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

### Complete Workflow

1. **(Optional) Generate Training Data from Real Datasets**:
   ```bash
   python generate_training_data.py
   ```
   This downloads and processes data from 20 Newsgroups and AG News datasets to create `training_data.csv`. This improves the classifier's accuracy significantly.

2. **Scan a Folder**: Navigate to the "Scan Folder" page and enter a local directory path
3. **Configure Options**: Choose whether to compute hashes, save to database, and extract content
4. **Set Exclusions**: Specify directories to exclude from the scan
5. **Review Results**: View scanned files, their metadata, and SHA-256 hashes
6. **Find Duplicates**: Use the Duplicate Finder to identify exact duplicate groups
7. **Analyze Similarity**: Use semantic similarity to find related documents
8. **Classify Files**: Use AI Organization to categorize documents automatically (check "Use Real Training Data" if you generated training_data.csv)
9. **Organize Files**: Preview and execute file organization with approval
10. **Search Files**: Use Search Explorer to find specific files
11. **View History**: Check History page for scan and action records
12. **Configure Settings**: Adjust application preferences in Settings page

## Supported File Formats

### Fully Supported
- Plain Text (.txt)
- Markdown (.md)
- CSV (.csv)
- JSON (.json)
- Python (.py)
- PDF (.pdf) - Text extraction implemented
- Microsoft Word (.docx) - Text extraction implemented

Note: PDF and DOCX extraction works for standard documents. OCR for scanned PDFs is not available.

## Training Data

### Synthetic Data (Default)
The classifier uses synthetic training data by default, which is sufficient for demonstration purposes but may not perform optimally on real-world documents.

### Real Datasets (Recommended)
For production use, generate training data from real datasets:

```bash
python generate_training_data.py
```

This script:
- Downloads data from 20 Newsgroups (via scikit-learn)
- Downloads data from AG News (via Hugging Face)
- Maps categories to the app's 8 predefined categories
- Creates `training_data.csv` with ~1000+ labeled examples

Once generated, check "Use Real Training Data" in the AI Organization page to use the improved classifier.

**Note**: Requires internet connection to download datasets on first run (~50MB total).

## AI Methodology

### Exact Duplicate Detection

Files are compared using SHA-256 cryptographic hashing. Matching hashes indicate byte-identical files.

### Semantic Similarity

Documents are converted to numerical vectors using Sentence Transformers (`all-MiniLM-L6-v2`). Cosine similarity identifies documents with similar content, even when wording differs.

### Document Classification

A combination of rule-based baseline and machine learning categorizes documents into:
- Work and Projects
- Education and Notes
- Finance and Bills
- Career and Resumes
- Personal Documents
- Software and Code
- Images and Media
- Miscellaneous

## Privacy and Security

- **Local-First Processing**: All analysis happens on your machine
- **No Cloud Uploads**: Document contents are never sent to external services
- **No Automatic Deletion**: Files are never deleted without explicit approval
- **Reversible Operations**: All file moves can be undone
- **Path Validation**: Operations are restricted to authorized directories

## Testing

Run the test suite:

```bash
pytest -q
```

Run linting:

```bash
ruff check .
```

## Known Limitations

- Initial ML classifier uses a rule-based baseline; training data will be added in Phase 5
- Semantic similarity requires downloading embedding models on first run
- OCR for scanned PDFs is not yet implemented
- Large collections (>10,000 documents) may require performance optimization

## Roadmap

- [x] Phase 1: Repository foundation
- [x] Phase 2: File scanning and database
- [ ] Phase 3: Document extraction and hashing
- [ ] Phase 4: Frontend MVP
- [ ] Phase 5: AI classification
- [ ] Phase 6: Semantic similarity
- [ ] Phase 7: Organization and recovery
- [ ] Phase 8: Search, history, and reports
- [ ] Phase 9: Hardening and release

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system architecture and component design.

## User Guide

See [USER_GUIDE.md](docs/USER_GUIDE.md) for detailed usage instructions.

## Security

See [SECURITY.md](docs/SECURITY.md) for security considerations and best practices.
