"""Tests for the reporting service."""

from src.ai_clutter_cleaner.services.reporting import generate_csv_report, generate_report


def test_generate_report_empty():
    """Test generating a report with no results."""
    report = generate_report([])

    assert "No scan results to report" in report


def test_generate_report_with_data():
    """Test generating a report with scan results."""
    scan_results = [
        {"name": "file1.txt", "path": "/docs/file1.txt", "extension": ".txt", "size": 1000},
        {"name": "file2.pdf", "path": "/docs/file2.pdf", "extension": ".pdf", "size": 50000},
    ]

    report = generate_report(scan_results)

    assert "SUMMARY" in report
    assert "Total Files: 2" in report
    assert "FILE TYPE BREAKDOWN" in report
    assert ".txt" in report
    assert ".pdf" in report


def test_generate_csv_report():
    """Test generating a CSV report."""
    scan_results = [
        {"name": "file1.txt", "path": "/docs/file1.txt", "extension": ".txt", "size": 1000},
    ]

    csv = generate_csv_report(scan_results)

    assert "name,path,extension,size_kb" in csv
    assert "file1.txt" in csv
    assert ".txt" in csv
