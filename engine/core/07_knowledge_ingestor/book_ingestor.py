"""Book Knowledge Ingestor - Parse txt books and map insights to BOS-FS knowledge layers."""

import argparse
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class BookChapter:
    """Represents a parsed chapter from a book."""
    title: str
    start_line: int
    end_line: int = -1
    content: str = ""


class BookIngestor:
    """Full pipeline: read book → parse TOC → split chapters → extract insights → map to BOS-FS layers."""

    # Chapter markers ordered by specificity (highest priority first)
    CHAPTER_PATTERNS = [
        # "Chapter One:", "Chapter 1:", "Chapter Two - Title"
        re.compile(
            r'^(?:Chapter)\s+(?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|'
            r'Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty|'
            r'\d+)\s*[:.\-–—]\s*(.+)',
            re.IGNORECASE | re.MULTILINE,
        ),
        # "PART 1:", "PART I:", "PART ONE:", "PART I Title" (no separator)
        re.compile(
            r'^(?:PART)\s+(?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|'
            r'I{1,3}|IV|V|VI{0,3}|IX|X|\d+)\s*[:.\-–—]?\s*(.+)',
            re.IGNORECASE | re.MULTILINE,
        ),
        # Standalone "Chapter N" without colon (less specific)
        re.compile(
            r'^(?:Chapter)\s+(?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|'
            r'Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty|'
            r'\d+)\s*$',
            re.IGNORECASE | re.MULTILINE,
        ),
    ]

    # BOS-FS layer keyword mapping
    LAYER_KEYWORDS: Dict[str, List[str]] = {
        "intent": [
            "persona", "user", "customer", "value", "vision", "goal", "problem",
            "why", "purpose", "mission", "need", "demand", "user story",
            "job to be done", "opportunity", "outcome", "desirability",
        ],
        "runtime": [
            "workflow", "process", "habit", "routine", "cadence", "cycle",
            "iteration", "loop", "rhythm", "flow", "daily", "weekly",
            "continuous", "feedback", "rhythm", "pace",
        ],
        "execution": [
            "template", "checklist", "step", "sop", "guide", "how to",
            "practice", "technique", "method", "recipe", "pattern",
            "tactic", "action", "implement", "build",
        ],
        "governance": [
            "metric", "measure", "kpi", "quality", "review", "standard",
            "rule", "criteria", "rubric", "audit", "compliance",
            "threshold", "benchmark", "evaluate", "assess",
        ],
        "adoption": [
            "adopt", "diffusion", "spread", "scale", "transform",
            "change", "migration", "onboarding", "train", "culture",
            "differentiate", "position", "strategy",
        ],
    }

    def parse_toc(self, text: str) -> List[Tuple[int, str]]:
        """Parse text to find all chapter/part markers.

        Args:
            text: Full book text.

        Returns:
            List of (line_index, chapter_title) tuples sorted by line position.
        """
        lines = text.split("\n")
        markers: List[Tuple[int, str]] = []

        # Strategy 1: Look for "Chapter X: Title" or "Chapter X" patterns
        for pattern in self.CHAPTER_PATTERNS:
            for match in pattern.finditer(text):
                line_index = text[:match.start()].count("\n")
                title = match.group(1).strip() if match.groups() else match.group(0).strip()
                # Deduplicate: skip if this line already has a marker
                if not any(idx == line_index for idx, _ in markers):
                    markers.append((line_index, title))

        # Sort by line position
        markers.sort(key=lambda x: x[0])
        return markers

    def split_chapters(self, text: str) -> List[BookChapter]:
        """Split book text into chapters using TOC markers.

        Args:
            text: Full book text.

        Returns:
            List of BookChapter objects.
        """
        markers = self.parse_toc(text)
        if not markers:
            # No markers found — treat entire book as a single chapter
            return [BookChapter(title="Full Book", start_line=0, end_line=-1, content=text)]

        lines = text.split("\n")
        chapters: List[BookChapter] = []

        for i, (start_line, title) in enumerate(markers):
            # End at next marker or end of file
            if i + 1 < len(markers):
                end_line = markers[i + 1][0] - 1
            else:
                end_line = len(lines) - 1

            chapter_lines = lines[start_line:end_line + 1]
            content = "\n".join(chapter_lines)

            chapters.append(BookChapter(
                title=title,
                start_line=start_line,
                end_line=end_line,
                content=content,
            ))

        return chapters

    def extract_insights(self, chapter_text: str) -> Dict[str, List[str]]:
        """Extract core concepts, methodologies, actionable steps, and key metrics.

        Args:
            chapter_text: A single chapter's text content.

        Returns:
            Dict with keys: core_concepts, methodologies, actionable_steps, key_metrics.
        """
        insights: Dict[str, List[str]] = {
            "core_concepts": [],
            "methodologies": [],
            "actionable_steps": [],
            "key_metrics": [],
        }

        sentences = re.split(r'(?<=[.!?])\s+', chapter_text.replace("\n", " "))

        # Extract core concepts: sentences with key idea / principle / framework
        concept_keywords = [
            "key idea", "principle", "framework", "concept", "core",
            "fundamental", "essential", "definition", "means", "refers to",
        ]
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in concept_keywords):
                cleaned = sentence.strip()
                if cleaned and len(cleaned) > 20 and len(insights["core_concepts"]) < 5:
                    insights["core_concepts"].append(cleaned)

        # Extract methodologies: step-by-step or process descriptions
        method_keywords = [
            "method", "approach", "process", "step-by-step", "phase",
            "stage", "technique", "practice", "pattern", "strategy",
            "first", "second", "third", "finally", "then", "next",
        ]
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in method_keywords):
                cleaned = sentence.strip()
                if cleaned and len(cleaned) > 30 and len(insights["methodologies"]) < 5:
                    insights["methodologies"].append(cleaned)

        # Extract actionable steps: imperatives / action items
        action_keywords = [
            "should", "must", "need to", "do this", "action item",
            "make sure", "ensure", "remember to", "try to",
            "start by", "begin with", "focus on",
        ]
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in action_keywords):
                cleaned = sentence.strip()
                if cleaned and len(cleaned) > 20 and len(insights["actionable_steps"]) < 5:
                    insights["actionable_steps"].append(cleaned)

        # Extract key metrics: measurable indicators
        metric_keywords = [
            "metric", "measure", "kpi", "indicator", "rate",
            "percentage", "lead time", "cycle time", "throughput",
            "deployment frequency", "change fail", "mean time",
            "score", "ratio", "benchmark",
        ]
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in metric_keywords):
                cleaned = sentence.strip()
                if cleaned and len(cleaned) > 20 and len(insights["key_metrics"]) < 5:
                    insights["key_metrics"].append(cleaned)

        return insights

    def map_to_bosfs(self, insights: Dict[str, List[str]]) -> Dict[str, Dict[str, List[str]]]:
        """Map extracted insights to BOS-FS five layers.

        Args:
            insights: Dict from extract_insights().

        Returns:
            Dict mapping layer name → {core_concepts, methodologies, actionable_steps, key_metrics}.
        """
        layer_map: Dict[str, Dict[str, List[str]]] = {
            "intent": {"core_concepts": [], "methodologies": [], "actionable_steps": [], "key_metrics": []},
            "runtime": {"core_concepts": [], "methodologies": [], "actionable_steps": [], "key_metrics": []},
            "execution": {"core_concepts": [], "methodologies": [], "actionable_steps": [], "key_metrics": []},
            "governance": {"core_concepts": [], "methodologies": [], "actionable_steps": [], "key_metrics": []},
            "adoption": {"core_concepts": [], "methodologies": [], "actionable_steps": [], "key_metrics": []},
        }

        for insight_type, items in insights.items():
            for item in items:
                item_lower = item.lower()
                best_layer = self._classify_layer(item_lower)
                layer_map[best_layer][insight_type].append(item)

        return layer_map

    def _classify_layer(self, text: str) -> str:
        """Classify a text snippet into the best-matching BOS-FS layer.

        Args:
            text: Lowercase text snippet.

        Returns:
            One of: intent, runtime, execution, governance, adoption.
        """
        scores: Dict[str, int] = {layer: 0 for layer in self.LAYER_KEYWORDS}

        for layer, keywords in self.LAYER_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    scores[layer] += 1

        # Return layer with highest score; default to "runtime" on tie
        best_layer = max(scores, key=scores.get)  # type: ignore[arg-type]
        if scores[best_layer] == 0:
            return "runtime"  # Default fallback
        return best_layer

    def ingest(self, book_path: str, output_dir: str = "knowledge/") -> Dict[str, List[str]]:
        """Full pipeline: read → parse → split → extract → map → write.

        Args:
            book_path: Path to the txt book file.
            output_dir: Base directory for knowledge output.

        Returns:
            Dict of {layer: [written_file_paths]}.

        Raises:
            FileNotFoundError: If book_path does not exist.
            ValueError: If book_path is not a .txt file.
        """
        if not os.path.isfile(book_path):
            raise FileNotFoundError(f"Book file not found: {book_path}")

        if not book_path.endswith(".txt"):
            raise ValueError(f"Expected .txt file, got: {book_path}")

        # Read with encoding fallback
        text = self._read_with_encoding(book_path)

        # Derive book name from filename
        book_name = os.path.splitext(os.path.basename(book_path))[0].strip()

        return self._process_book(text, book_name, output_dir)

    def ingest_batch(self, book_paths: List[str], output_dir: str = "knowledge/") -> Dict:
        """Batch ingestion with deduplication and merge.

        Args:
            book_paths: List of paths to txt book files.
            output_dir: Base directory for knowledge output.

        Returns:
            Dict with keys: 'books' (list of book results), 'summary' (ingest_summary output).
        """
        book_results = []
        all_written: Dict[str, List[str]] = {
            "intent": [], "runtime": [], "execution": [], "governance": [], "adoption": [],
        }

        for book_path in book_paths:
            try:
                written = self.ingest(book_path, output_dir)
                book_name = os.path.splitext(os.path.basename(book_path))[0].strip()
                for layer, files in written.items():
                    all_written[layer].extend(files)
                book_results.append({
                    "book": book_name,
                    "path": book_path,
                    "status": "success",
                    "files": written,
                    "total_files": sum(len(v) for v in written.values()),
                })
            except (FileNotFoundError, ValueError) as e:
                book_results.append({
                    "book": os.path.basename(book_path),
                    "path": book_path,
                    "status": "error",
                    "error": str(e),
                    "files": {},
                    "total_files": 0,
                })

        summary = self.ingest_summary(book_results)
        return {"books": book_results, "summary": summary}

    def ingest_summary(self, book_results: List[Dict]) -> str:
        """Generate ingestion summary report.

        Args:
            book_results: List of book ingestion results from ingest() or ingest_batch().

        Returns:
            Formatted summary string.
        """
        lines = [
            "# BOS-FS Knowledge Ingestion Summary",
            "",
            f"## Overview",
            f"- **Books processed**: {len(book_results)}",
            f"- **Successful**: {sum(1 for b in book_results if b['status'] == 'success')}",
            f"- **Failed**: {sum(1 for b in book_results if b['status'] == 'error')}",
            "",
        ]

        # Layer statistics
        layer_stats: Dict[str, int] = {
            "intent": 0, "runtime": 0, "execution": 0, "governance": 0, "adoption": 0,
        }
        all_files: Dict[str, List[str]] = {
            "intent": [], "runtime": [], "execution": [], "governance": [], "adoption": [],
        }

        for book in book_results:
            if book["status"] == "success":
                for layer, files in book["files"].items():
                    layer_stats[layer] += len(files)
                    all_files[layer].extend(files)

        lines.append("## Knowledge Files by Layer")
        lines.append("| Layer | Files |")
        lines.append("|-------|-------|")
        for layer, count in layer_stats.items():
            lines.append(f"| {layer} | {count} |")
        lines.append(f"| **Total** | **{sum(layer_stats.values())}** |")
        lines.append("")

        # Coverage matrix (Books × Layers)
        lines.append("## Coverage Matrix (Books × Layers)")
        lines.append("| Book | Intent | Runtime | Execution | Governance | Adoption |")
        lines.append("|------|--------|---------|-----------|------------|----------|")

        for book in book_results:
            if book["status"] == "success":
                counts = {layer: len(book["files"].get(layer, [])) for layer in layer_stats}
                lines.append(
                    f"| {book['book'][:50]} "
                    f"| {counts['intent']} | {counts['runtime']} "
                    f"| {counts['execution']} | {counts['governance']} "
                    f"| {counts['adoption']} |"
                )
            else:
                lines.append(f"| {book['book'][:50]} | ERROR: {book['error'][:30]} |")
        lines.append("")

        # Generated file list
        lines.append("## Generated Files")
        for layer in layer_stats:
            if all_files[layer]:
                lines.append(f"\n### {layer}")
                for f in all_files[layer]:
                    lines.append(f"- {f}")
        lines.append("")

        return "\n".join(lines)

    def _process_book(self, text: str, book_name: str, output_dir: str) -> Dict[str, List[str]]:
        """Internal: process book text into knowledge files."""
        # Split chapters
        chapters = self.split_chapters(text)

        # Process each chapter
        written_files: Dict[str, List[str]] = {
            "intent": [], "runtime": [], "execution": [], "governance": [], "adoption": [],
        }

        for chapter in chapters:
            insights = self.extract_insights(chapter.content)
            layer_map = self.map_to_bosfs(insights)

            for layer_name, layer_insights in layer_map.items():
                # Skip layers with no content for this chapter
                total_items = sum(len(v) for v in layer_insights.values())
                if total_items == 0:
                    continue

                # Write knowledge file
                topic_slug = self._slugify(chapter.title)
                output_path = os.path.join(output_dir, layer_name, f"{topic_slug}.md")
                content = self._format_knowledge_page(
                    chapter_title=chapter.title,
                    book_name=book_name,
                    layer=layer_name,
                    insights=layer_insights,
                )

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)

                written_files[layer_name].append(output_path)

        return written_files

    def _read_with_encoding(self, path: str) -> str:
        """Read file with UTF-8 → GBK → Latin-1 encoding fallback."""
        for encoding in ["utf-8", "gbk", "latin-1"]:
            try:
                with open(path, "r", encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        # Last resort
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert a title to a filename-safe slug (Windows-compatible, max 150 chars)."""
        slug = text.lower().strip()
        slug = re.sub(r'[^a-z0-9\s_\-]', '', slug)
        slug = re.sub(r'\s+', '_', slug)
        slug = re.sub(r'_+', '_', slug)
        slug = slug.strip("_")
        # Windows filename max is 255, but be conservative
        if len(slug) > 150:
            slug = slug[:140] + "_" + slug[-9:]
        return slug if slug else "untitled"

    @staticmethod
    def _format_knowledge_page(
        chapter_title: str,
        book_name: str,
        layer: str,
        insights: Dict[str, List[str]],
    ) -> str:
        """Format a knowledge page in the BOS-FS output schema."""
        lines = [
            f"# {chapter_title}",
            f"> Source: {book_name}",
            f"> Layer: {layer}",
            "",
        ]

        # Core Concepts
        if insights.get("core_concepts"):
            lines.append("## Core Concepts")
            for concept in insights["core_concepts"]:
                lines.append(f"- {concept}")
            lines.append("")

        # Methodologies
        if insights.get("methodologies"):
            lines.append("## Methodology")
            for i, method in enumerate(insights["methodologies"], 1):
                lines.append(f"{i}. {method}")
            lines.append("")

        # Actionable Steps
        if insights.get("actionable_steps"):
            lines.append("## Actionable Steps")
            for step in insights["actionable_steps"]:
                lines.append(f"- [ ] {step}")
            lines.append("")

        # Key Metrics
        if insights.get("key_metrics"):
            lines.append("## Key Metrics")
            lines.append("| Metric | Definition | Target |")
            lines.append("|--------|------------|--------|")
            for metric in insights["key_metrics"]:
                lines.append(f"| {metric} | — | — |")
            lines.append("")

        return "\n".join(lines)


def main():
    """CLI entry point: python -m engine.core.07_knowledge_ingestor.book_ingestor ingest|batch ..."""
    parser = argparse.ArgumentParser(description="BOS-FS Book Knowledge Ingestor")
    subparsers = parser.add_subparsers(dest="command")

    ingest_parser = subparsers.add_parser("ingest", help="Ingest a single book")
    ingest_parser.add_argument("book_path", help="Path to the txt book file")
    ingest_parser.add_argument(
        "--output-dir", "-o", default="knowledge/",
        help="Output directory for knowledge files (default: knowledge/)",
    )

    batch_parser = subparsers.add_parser("batch", help="Ingest multiple books")
    batch_parser.add_argument("book_paths", nargs="+", help="Paths to book txt files")
    batch_parser.add_argument(
        "--output-dir", "-o", default="knowledge/",
        help="Output directory for knowledge files (default: knowledge/)",
    )
    batch_parser.add_argument(
        "--summary-output", "-s", default=None,
        help="Path to write summary report (default: stdout)",
    )

    args = parser.parse_args()

    ingestor = BookIngestor()

    if args.command == "ingest":
        try:
            written = ingestor.ingest(args.book_path, args.output_dir)
            total = sum(len(v) for v in written.values())
            print(f"Ingested: {args.book_path}")
            print(f"Generated {total} knowledge files:")
            for layer, files in written.items():
                if files:
                    print(f"  [{layer}] {len(files)} file(s)")
                    for f in files:
                        print(f"    → {f}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "batch":
        result = ingestor.ingest_batch(args.book_paths, args.output_dir)
        summary = result["summary"]

        if args.summary_output:
            os.makedirs(os.path.dirname(args.summary_output) or ".", exist_ok=True)
            with open(args.summary_output, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"Summary written to: {args.summary_output}")
        else:
            print(summary)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
