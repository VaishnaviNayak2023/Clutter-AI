"""Reporting service."""

from datetime import datetime


def generate_report(scan_results: list) -> str:
    """
    Generate a summary report of scan results.

    Args:
        scan_results: List of scan results (FileMetadata or dicts)

    Returns:
        Formatted report string
    """
    if not scan_results:
        return "No scan results to report."

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("AI DIGITAL CLUTTER CLEANER - SCAN REPORT")
    report_lines.append("=" * 60)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Summary statistics
    total_files = len(scan_results)
    total_size = sum(f.get("size", f.size if hasattr(f, "size") else 0) for f in scan_results)
    total_size_mb = total_size / 1_000_000

    report_lines.append("SUMMARY")
    report_lines.append("-" * 40)
    report_lines.append(f"Total Files: {total_files}")
    report_lines.append(f"Total Size: {total_size_mb:.2f} MB")
    report_lines.append("")

    # File type breakdown
    extension_counts = {}
    for f in scan_results:
        ext = f.get("extension", f.extension if hasattr(f, "extension") else "unknown")
        extension_counts[ext] = extension_counts.get(ext, 0) + 1

    report_lines.append("FILE TYPE BREAKDOWN")
    report_lines.append("-" * 40)
    for ext, count in sorted(extension_counts.items()):
        report_lines.append(f"{ext:15} : {count}")
    report_lines.append("")

    # Size distribution
    size_ranges = {
        "< 1 KB": 0,
        "1-10 KB": 0,
        "10-100 KB": 0,
        "100 KB - 1 MB": 0,
        "> 1 MB": 0,
    }

    for f in scan_results:
        size = f.get("size", f.size if hasattr(f, "size") else 0)
        size_kb = size / 1_000

        if size_kb < 1:
            size_ranges["< 1 KB"] += 1
        elif size_kb < 10:
            size_ranges["1-10 KB"] += 1
        elif size_kb < 100:
            size_ranges["10-100 KB"] += 1
        elif size_kb < 1000:
            size_ranges["100 KB - 1 MB"] += 1
        else:
            size_ranges["> 1 MB"] += 1

    report_lines.append("SIZE DISTRIBUTION")
    report_lines.append("-" * 40)
    for range_name, count in size_ranges.items():
        report_lines.append(f"{range_name:15} : {count}")
    report_lines.append("")

    report_lines.append("=" * 60)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 60)

    return "\n".join(report_lines)


def generate_csv_report(scan_results: list) -> str:
    """
    Generate a CSV report of scan results.

    Args:
        scan_results: List of scan results

    Returns:
        CSV-formatted string
    """
    if not scan_results:
        return "name,path,extension,size_kb\n"

    lines = ["name,path,extension,size_kb"]

    for f in scan_results:
        name = f.get("name", f.name if hasattr(f, "name") else "")
        path = f.get("path", f.path if hasattr(f, "path") else "")
        ext = f.get("extension", f.extension if hasattr(f, "extension") else "")
        size = f.get("size", f.size if hasattr(f, "size") else 0)
        size_kb = size / 1_000

        lines.append(f'"{name}","{path}","{ext}",{size_kb:.2f}')

    return "\n".join(lines)
