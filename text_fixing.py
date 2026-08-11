import re
from rapidfuzz import fuzz

def normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation noise."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # drop punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text

def reconstruct_text(rec_texts, rec_boxes, y_tol=10):
    """Sort fragments into reading order (top-to-bottom, left-to-right)
    and join them into one string."""
    items = list(zip(rec_texts, rec_boxes))

    # box format from PaddleOCR predict(): [x1, y1, x2, y2]
    items.sort(key=lambda it: (it[1][1], it[1][0]))

    lines, current_line, current_y = [], [], None
    for text, box in items:
        y_center = (box[1] + box[3]) / 2
        if current_y is None or abs(y_center - current_y) <= y_tol:
            current_line.append((text, box))
            current_y = y_center if current_y is None else current_y
        else:
            current_line.sort(key=lambda it: it[1][0])
            lines.append(" ".join(t for t, _ in current_line))
            current_line = [(text, box)]
            current_y = y_center
    if current_line:
        current_line.sort(key=lambda it: it[1][0])
        lines.append(" ".join(t for t, _ in current_line))

    return " ".join(lines)

def is_paragraph_in_image(paragraph, reconstructed_text, threshold=85):
    ocr_blob = normalize(reconstructed_text)
    target = normalize(paragraph)

    # Fuzzy substring check: partial_ratio finds the best-aligned
    # substring match even if lengths differ
    score = fuzz.partial_ratio(target, ocr_blob)
    return score >= threshold, score