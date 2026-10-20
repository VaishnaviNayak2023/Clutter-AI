# Architecture

## System Overview

The AI Digital Clutter Cleaner follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│              (Streamlit Dashboard & Pages)              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Application Layer                       │
│         (Services: Scanner, Extractor, Classifier)      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Domain Layer                          │
│            (Models: FileMetadata, Prediction, etc.)      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               Infrastructure Layer                       │
│        (Database, Filesystem, Model Loading, Logging)    │
└─────────────────────────────────────────────────────────┘
```

## Components

### Presentation Layer

- **app.py**: Main application entry point with navigation
- **pages/**: Individual Streamlit pages for different features
  - 1_Scan_Folder.py: Folder scanning interface
  - 2_AI_Organization.py: Category review and approval
  - 3_Duplicate_Finder.py: Duplicate detection review
  - 4_Search_Explorer.py: File search interface
  - 5_History.py: Action history and undo
  - 6_Settings.py: Configuration management

### Application Layer

**Services:**
- **scanner.py**: Recursive file discovery and metadata collection
- **extractor.py**: Text extraction from supported document formats
- **hashing.py**: SHA-256 computation for duplicate detection
- **classifier.py**: Document categorization (ML + rule-based)
- **embeddings.py**: Semantic embedding generation and similarity
- **duplicates.py**: Exact and semantic duplicate grouping
- **organizer.py**: Destination planning and file operations
- **history.py**: Action recording and undo functionality
- **search.py**: File search and filtering
- **reporting.py**: Report generation and export

### Domain Layer

**Data Models:**
- **FileMetadata**: File information (name, path, size, hash, etc.)
- **ScanResult**: Results of a folder scan
- **CategoryPrediction**: AI classification with confidence
- **SimilarityMatch**: Semantic similarity between documents

### Infrastructure Layer

**Database:**
- **connection.py**: SQLite connection management
- **schema.py**: Database schema definitions
- **repositories.py**: Data access layer

**Utilities:**
- **paths.py**: Path validation and resolution
- **file_types.py**: File type checking
- **logging_config.py**: Logging setup

## Data Flow

### Scanning Flow

1. User selects folder in UI
2. Scanner service enumerates files
3. Metadata collected for each file
4. SHA-256 hashes computed
5. Results stored in database
6. UI displays scan results

### Classification Flow

1. Extractor service reads document text
2. Classifier service predicts category
3. Confidence score calculated
4. Prediction stored in database
5. UI shows category recommendations

### Organization Flow

1. User reviews proposals in UI
2. Organizer service validates destinations
3. Dry-run mode shows impact preview
4. User approves selected actions
5. File operations executed safely
6. History service records actions
7. Undo available for reversible operations

## Database Schema

### Tables

- **files**: File metadata and hashes
- **predictions**: AI category predictions
- **embeddings**: Semantic embedding storage
- **similarity_matches**: Document similarity pairs
- **scan_jobs**: Scan history and status
- **file_actions**: Performed file operations
- **settings**: Application configuration

## Security Considerations

- All file operations validated against authorized root
- Path traversal prevention
- No automatic file deletion
- Explicit user approval required for moves
- Reversible operations with undo capability
- Local-only processing (no cloud uploads)

## Performance Considerations

- Chunked file reading for hashing
- Batch embedding generation
- Caching of expensive operations
- Incremental scanning support
- Configurable resource limits
