
def remove_unverified_price_content(text):
    """Remove AI-generated expense sections and budget claims."""

    lines = text.splitlines()
    cleaned_lines = []
    skip_expenses = False

    expense_headings = (
        "approximate expense categories",
        "expense categories",
        "expense estimates",
        "estimated expenses",
        "budget summary",
        "estimated budget breakdown",
        "cost breakdown",
        "total estimated cost",
        "total estimated expense",
        "total estimated expenses",
        "total estimated budget",
    )

    next_section_headings = (
        "recommended destination",
        "important places to visit",
        "popular activities",
        "suitable areas to stay",
        "general travel tips",
        "trip summary",
        "day-by-day itinerary",
        "flight information",
        "accommodation",
        "activities",
        "safety tips",
        "money-saving suggestions",
    )

    for line in lines:
        stripped = line.strip()
        normalized = stripped.lower()

        # Recognize headings written as **Heading:**,
        # ## Heading, or ordinary Heading:
        heading_text = normalized
        heading_text = heading_text.lstrip("#").strip()
        heading_text = heading_text.strip("*").strip()
        heading_text = heading_text.rstrip(":").strip()

        if any(
            heading_text.startswith(heading)
            for heading in expense_headings
        ):
            skip_expenses = True
            continue

        if skip_expenses:
            if any(
                heading_text.startswith(heading)
                for heading in next_section_headings
            ):
                skip_expenses = False
            else:
                continue

        # Remove unsupported monetary claims outside the
        # expense section too.
        if "₹" in line:
            continue

        if re.search(
            r"(?i)\b(?:"
            r"this travel plan should fit your budget|"
            r"this plan should fit your budget|"
            r"fits your budget|"
            r"leaving room for flexibility|"
            r"total estimated cost|"
            r"total estimated expense|"
            r"total estimated expenses"
            r")\b",
            line,
        ):
            continue

        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()
