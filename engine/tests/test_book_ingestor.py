"""Tests for BookIngestor module."""

import unittest
import os
import sys
import tempfile
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load_book_ingestor():
    """Load BookIngestor and BookChapter from file path."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, "core", "07_knowledge_ingestor", "book_ingestor.py")
    spec = importlib.util.spec_from_file_location("book_ingestor", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BookIngestor, mod.BookChapter


class TestParseTOC(unittest.TestCase):
    """Tests for parse_toc method."""

    def setUp(self):
        BookIngestor, _ = _load_book_ingestor()
        self.ingestor = BookIngestor()

    def test_parse_chapter_numbered(self):
        text = """Some intro text.

Chapter 1: The Problem with Org Charts
Communication Structures of an Organization

Chapter 2: Conway's Law and Why It Matters
Understanding Conway's Law

Chapter 3: Team-First Thinking
Use Small Teams
"""
        markers = self.ingestor.parse_toc(text)
        self.assertEqual(len(markers), 3)
        self.assertIn("The Problem with Org Charts", markers[0][1])
        self.assertIn("Conway's Law and Why It Matters", markers[1][1])
        self.assertIn("Team-First Thinking", markers[2][1])

    def test_parse_chapter_words(self):
        text = """Chapter One: Getting Started
Some content here.

Chapter Two: Building the Product
More content here.
"""
        markers = self.ingestor.parse_toc(text)
        self.assertEqual(len(markers), 2)
        self.assertIn("Getting Started", markers[0][1])
        self.assertIn("Building the Product", markers[1][1])

    def test_parse_part_markers(self):
        text = """PART 1: Teams as the Means of Delivery
Chapter 1: Intro

PART 2: Team Topologies That Work
Chapter 4: Static Topologies
"""
        markers = self.ingestor.parse_toc(text)
        self.assertGreaterEqual(len(markers), 4)
        # Should find PART markers and Chapter markers
        titles = [t for _, t in markers]
        self.assertTrue(any("Teams as the Means" in t for t in titles))

    def test_parse_no_markers(self):
        text = "This is just plain text without any chapters."
        markers = self.ingestor.parse_toc(text)
        self.assertEqual(len(markers), 0)

    def test_parse_realistic_toc(self):
        text = """CONTENTS

Chapter 1: The Problem with Org Charts
Communication Structures of an Organization
Team Topologies: A New Way of Thinking about Teams

Chapter 2: Conway's Law and Why It Matters
Understanding and Using Conway's Law
The Reverse Conway Maneuver

PART II TEAM TOPOLOGIES THAT WORK FOR FLOW

Chapter 4: Static Team Topologies
Team Anti-Patterns
Design for Flow of Change
"""
        markers = self.ingestor.parse_toc(text)
        # Should find Chapter 1, Chapter 2, PART II, Chapter 4
        self.assertGreaterEqual(len(markers), 4)


class TestSplitChapters(unittest.TestCase):
    """Tests for split_chapters method."""

    def setUp(self):
        BookIngestor, _ = _load_book_ingestor()
        self.ingestor = BookIngestor()

    def test_split_multiple_chapters(self):
        text = """Intro paragraph.

Chapter 1: First Chapter
This is the content of chapter 1.
It has multiple lines.

Chapter 2: Second Chapter
This is the content of chapter 2.

Chapter 3: Third Chapter
Final chapter content.
"""
        chapters = self.ingestor.split_chapters(text)
        self.assertEqual(len(chapters), 3)
        self.assertIn("First Chapter", chapters[0].title)
        self.assertIn("Second Chapter", chapters[1].title)
        self.assertIn("Third Chapter", chapters[2].title)
        self.assertIn("content of chapter 1", chapters[0].content)
        self.assertIn("content of chapter 2", chapters[1].content)

    def test_split_no_chapters(self):
        text = "This book has no chapter markers at all."
        chapters = self.ingestor.split_chapters(text)
        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0].title, "Full Book")
        self.assertEqual(chapters[0].content, text)

    def test_split_chapter_content_boundaries(self):
        text = """Chapter 1: Alpha
Content of Alpha chapter.
End of Alpha.

Chapter 2: Beta
Content of Beta chapter.
End of Beta.
"""
        chapters = self.ingestor.split_chapters(text)
        self.assertEqual(len(chapters), 2)
        # Chapter 1 should NOT contain "Beta"
        self.assertNotIn("Chapter 2", chapters[0].content)
        # Chapter 2 should contain its own content
        self.assertIn("Content of Beta", chapters[1].content)

    def test_chapter_dataclass(self):
        _, BookChapter = _load_book_ingestor()
        chapter = BookChapter(title="Test", start_line=5, end_line=10, content="Hello")
        self.assertEqual(chapter.title, "Test")
        self.assertEqual(chapter.start_line, 5)
        self.assertEqual(chapter.end_line, 10)
        self.assertEqual(chapter.content, "Hello")


class TestExtractInsights(unittest.TestCase):
    """Tests for extract_insights method."""

    def setUp(self):
        BookIngestor, _ = _load_book_ingestor()
        self.ingestor = BookIngestor()

    def test_extract_core_concepts(self):
        text = """The key idea of this framework is that teams should be small.
This principle guides our decision making process.
A fundamental concept in product management is understanding user needs.
Short sentence.
"""
        insights = self.ingestor.extract_insights(text)
        self.assertGreater(len(insights["core_concepts"]), 0)

    def test_extract_methodologies(self):
        text = """The first step in the process is to identify user problems.
Our approach to discovery involves continuous interviewing.
The second phase focuses on solution exploration.
"""
        insights = self.ingestor.extract_insights(text)
        self.assertGreater(len(insights["methodologies"]), 0)

    def test_extract_actionable_steps(self):
        text = """You should always validate assumptions before building features.
Teams must ensure they have clear boundaries to minimize cognitive load.
Start by mapping your current team interactions.
"""
        insights = self.ingestor.extract_insights(text)
        self.assertGreater(len(insights["actionable_steps"]), 0)

    def test_extract_key_metrics(self):
        text = """Lead time is the key metric for measuring delivery speed.
Deployment frequency is another important indicator of team performance.
The change failure rate measures quality of deployments.
"""
        insights = self.ingestor.extract_insights(text)
        self.assertGreater(len(insights["key_metrics"]), 0)

    def test_extract_empty_text(self):
        insights = self.ingestor.extract_insights("")
        self.assertEqual(insights["core_concepts"], [])
        self.assertEqual(insights["methodologies"], [])
        self.assertEqual(insights["actionable_steps"], [])
        self.assertEqual(insights["key_metrics"], [])

    def test_extract_all_dimensions_present(self):
        text = """The key idea is that small teams perform better.
The first step in our process is team design.
You should always measure cognitive load.
Lead time is the primary metric for delivery.
"""
        insights = self.ingestor.extract_insights(text)
        self.assertIn("core_concepts", insights)
        self.assertIn("methodologies", insights)
        self.assertIn("actionable_steps", insights)
        self.assertIn("key_metrics", insights)


class TestMapToBOSFS(unittest.TestCase):
    """Tests for map_to_bosfs method."""

    def setUp(self):
        BookIngestor, _ = _load_book_ingestor()
        self.ingestor = BookIngestor()

    def test_map_intent_keywords(self):
        insights = {
            "core_concepts": ["The key idea is understanding user value and customer persona"],
            "methodologies": [],
            "actionable_steps": [],
            "key_metrics": [],
        }
        layer_map = self.ingestor.map_to_bosfs(insights)
        # User value / customer persona → intent
        self.assertGreater(len(layer_map["intent"]["core_concepts"]), 0)

    def test_map_execution_keywords(self):
        insights = {
            "core_concepts": [],
            "methodologies": ["The step-by-step technique for building a template checklist"],
            "actionable_steps": [],
            "key_metrics": [],
        }
        layer_map = self.ingestor.map_to_bosfs(insights)
        # Template / checklist / step → execution
        self.assertGreater(len(layer_map["execution"]["methodologies"]), 0)

    def test_map_governance_keywords(self):
        insights = {
            "core_concepts": [],
            "methodologies": [],
            "actionable_steps": [],
            "key_metrics": ["Lead time is the primary KPI metric for quality review"],
        }
        layer_map = self.ingestor.map_to_bosfs(insights)
        # Metric / KPI / quality → governance
        self.assertGreater(len(layer_map["governance"]["key_metrics"]), 0)

    def test_map_five_layers_exist(self):
        insights = {
            "core_concepts": ["Test concept"],
            "methodologies": [],
            "actionable_steps": [],
            "key_metrics": [],
        }
        layer_map = self.ingestor.map_to_bosfs(insights)
        self.assertIn("intent", layer_map)
        self.assertIn("runtime", layer_map)
        self.assertIn("execution", layer_map)
        self.assertIn("governance", layer_map)
        self.assertIn("adoption", layer_map)

    def test_map_empty_insights(self):
        insights = {
            "core_concepts": [],
            "methodologies": [],
            "actionable_steps": [],
            "key_metrics": [],
        }
        layer_map = self.ingestor.map_to_bosfs(insights)
        for layer_name, layer_insights in layer_map.items():
            self.assertEqual(len(layer_insights["core_concepts"]), 0)

    def test_classify_layer_default(self):
        # Text with no keywords should default to "runtime"
        result = self.ingestor._classify_layer("some random text with no keywords")
        self.assertEqual(result, "runtime")


class TestFullIngestPipeline(unittest.TestCase):
    """Tests for the full ingest pipeline with mock books."""

    def setUp(self):
        BookIngestor, _ = _load_book_ingestor()
        self.ingestor = BookIngestor()
        self.temp_dir = tempfile.mkdtemp()

    def _create_mock_book(self, content: str) -> str:
        path = os.path.join(self.temp_dir, "mock_book.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_ingest_full_pipeline(self):
        mock_book = """Chapter 1: User Discovery
The key idea is understanding customer value and persona needs.
The first step in our process is continuous interviewing.
You should always validate assumptions before building features.
Lead time is the primary metric for delivery quality review.

Chapter 2: Solution Design
A fundamental concept is the opportunity solution tree framework.
The approach to design involves iterative prototyping techniques.
Teams must ensure they follow the template checklist for execution.
Deployment frequency is another important KPI indicator measure.
"""
        path = self._create_mock_book(mock_book)
        output_dir = os.path.join(self.temp_dir, "knowledge")

        written = self.ingestor.ingest(path, output_dir)
        total = sum(len(v) for v in written.values())
        self.assertGreater(total, 0)

        # Verify files were written
        for layer, files in written.items():
            for fpath in files:
                self.assertTrue(os.path.isfile(fpath), f"Expected file: {fpath}")

    def test_ingest_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.ingestor.ingest("/nonexistent/path/book.txt")

    def test_ingest_non_txt_file(self):
        path = os.path.join(self.temp_dir, "book.md")
        with open(path, "w") as f:
            f.write("# Hello")
        with self.assertRaises(ValueError):
            self.ingestor.ingest(path)

    def test_ingest_creates_output_dirs(self):
        mock_book = """Chapter 1: Test
The key idea is user value and customer persona.
"""
        path = self._create_mock_book(mock_book)
        output_dir = os.path.join(self.temp_dir, "new_knowledge", "sub")
        written = self.ingestor.ingest(path, output_dir)
        # Should have created directories and written files
        for files in written.values():
            for fpath in files:
                self.assertTrue(os.path.isdir(os.path.dirname(fpath)))

    def test_ingest_realistic_book_content(self):
        """Test with content similar to actual NEED-PACK books."""
        mock_book = """Team Topologies

Chapter 1: The Problem with Org Charts
Communication Structures of an Organization define how teams interact.
The key idea is that Conway's Law shapes both software architecture and team design.
The first step in our process is to map current communication patterns.
You should always consider cognitive load when designing team boundaries.
Deployment frequency is a key metric for measuring team flow and delivery.

PART II TEAM TOPOLOGIES THAT WORK FOR FLOW

Chapter 4: Static Team Topologies
Team Anti-Patterns are common mistakes in organization design.
The approach to choosing a topology involves evaluating the value stream.
Teams must ensure they reduce dependencies to achieve faster flow.
The measure of success includes change failure rate and mean time to recovery.
"""
        path = self._create_mock_book(mock_book)
        output_dir = os.path.join(self.temp_dir, "knowledge")

        written = self.ingestor.ingest(path, output_dir)
        total = sum(len(v) for v in written.values())
        self.assertGreaterEqual(total, 3)  # At least 3 files from multiple chapters

        # Verify Chapter 1 and Chapter 4 are processed
        all_files = []
        for files in written.values():
            all_files.extend(files)

        # Should have created files for both chapters
        file_names = [os.path.basename(f) for f in all_files]
        self.assertTrue(any("problem_with_org" in n for n in file_names))
        self.assertTrue(any("static_team_topologies" in n for n in file_names))


class TestSlugify(unittest.TestCase):
    """Tests for _slugify helper."""

    def setUp(self):
        BookIngestor, _ = _load_book_ingestor()
        self.ingestor = BookIngestor()

    def test_slugify_simple(self):
        self.assertEqual(self.ingestor._slugify("Hello World"), "hello_world")

    def test_slugify_special_chars(self):
        self.assertEqual(self.ingestor._slugify("Team's API!"), "teams_api")

    def test_slugify_numbers(self):
        self.assertEqual(self.ingestor._slugify("Chapter 1: Intro"), "chapter_1_intro")

    def test_slugify_empty(self):
        self.assertEqual(self.ingestor._slugify(""), "untitled")

    def test_slugify_underscores(self):
        self.assertEqual(self.ingestor._slugify("Hello   World"), "hello_world")


if __name__ == "__main__":
    unittest.main()
