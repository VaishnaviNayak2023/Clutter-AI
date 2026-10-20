# Contributing to AI Digital Clutter Cleaner

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, constructive, and inclusive. We welcome contributors from all backgrounds and experience levels.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Feature description
   - Use case or motivation
   - Potential implementation approach

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest -q`
5. Run linting: `ruff check .`
6. Commit your changes with clear messages
7. Push to your fork: `git push origin feature/my-feature`
8. Create a pull request

### Development Guidelines

- Follow existing code style (use ruff)
- Write tests for new functionality
- Update documentation as needed
- Keep changes focused and atomic
- Add type hints where appropriate

### Testing

- Write unit tests for new functions
- Ensure all tests pass before submitting
- Test on multiple operating systems if possible

## Project Structure

```
ai-digital-clutter-cleaner/
├── app.py                 # Main Streamlit application
├── src/                   # Source code
│   └── ai_clutter_cleaner/
│       ├── services/      # Business logic
│       ├── database/      # Data persistence
│       └── utils/         # Utility functions
├── pages/                 # Streamlit pages
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Getting Started

See README.md for installation and setup instructions.

## Questions?

Feel free to open an issue for questions or discussion.
