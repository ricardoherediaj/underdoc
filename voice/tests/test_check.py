"""Deterministic gate tests for checks/check.py.

Stdlib only, matching the harness ethos (no pip installs). Run with:

    python3 -m unittest discover -s tests          # or: python3 tests/test_check.py

These lock the gates against regression. The gates are the executable spec
(SPEC.md §1.5), so a test failing here means a gate drifted, not that a test
is wrong. Each test documents the contract it pins.
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "checks"))

import check  # noqa: E402


def gate_status(result):
    return result["status"]


class ParseTests(unittest.TestCase):
    def test_frontmatter_keys(self):
        meta, body = check.parse(str(REPO / "pipeline" / "03_draft.md"))
        self.assertEqual(meta.get("bucket"), "builds")
        self.assertEqual(meta.get("status"), "drafting")
        self.assertTrue(body.strip())

    def test_title_with_colon_is_preserved(self):
        """parse() splits on the FIRST colon, so a colon inside the title survives."""
        import tempfile, os
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write('---\ntitle: "How to Look for a Mentor: In Tech"\nbucket: bridge\nstatus: drafting\n---\n\nBody here.\n')
            path = f.name
        try:
            meta, _ = check.parse(path)
            self.assertEqual(meta["title"], "How to Look for a Mentor: In Tech")
        finally:
            os.unlink(path)

    def test_no_frontmatter_returns_empty_meta(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("Just a body, no frontmatter.\n")
            path = f.name
        try:
            meta, body = check.parse(path)
            self.assertEqual(meta, {})
            self.assertIn("Just a body", body)
        finally:
            os.unlink(path)


class G01WordCountTests(unittest.TestCase):
    def test_never_fails(self):
        """G-01 warns, never fails — length is Ricardo's call (SPEC §4.1)."""
        for body in ("A tiny post.", "Sentence here. " * 400):  # ~2000 words
            self.assertNotEqual(gate_status(check.g01_word_count(body, "builds")), "FAIL")

    def test_in_band_passes(self):
        body = "This is a sentence about building things. " * 143  # ~1001 words
        self.assertEqual(gate_status(check.g01_word_count(body, "builds")), "PASS")

    def test_short_field_note_warns(self):
        self.assertEqual(gate_status(check.g01_word_count("Short note.", "field-notes")), "WARN")


class G02SectionsTests(unittest.TestCase):
    def test_never_fails(self):
        """G-02 warns, never fails — heading count does not track performance."""
        body = "\n".join(f"### Section {i}" for i in range(20))
        self.assertNotEqual(gate_status(check.g02_sections(body)), "FAIL")

    def test_dramatic_two_part_heading_warns(self):
        body = "## The Hidden Cost: Why Your Pipeline Is Lying\n\nText."
        result = check.g02_sections(body)
        self.assertEqual(gate_status(result), "WARN")
        self.assertIn("two-part headings", result["detail"])


class G03SignoffTests(unittest.TestCase):
    def test_canonical_passes(self):
        self.assertEqual(gate_status(check.g03_signoff("Body.\n\nTill next time, Ricardo.")), "PASS")

    def test_variant_warns(self):
        self.assertEqual(gate_status(check.g03_signoff("Body.\n\nTil next time, Ricardo.")), "WARN")

    def test_absence_fails(self):
        self.assertEqual(gate_status(check.g03_signoff("Body with no signoff.")), "FAIL")


class G04IRatioTests(unittest.TestCase):
    def test_i_over_we_passes(self):
        body = "I built this. I like it. I use it every day."
        self.assertEqual(gate_status(check.g04_i_we_ratio(body)), "PASS")

    def test_we_over_i_fails(self):
        body = "We built this. We like it. Our team ships it."
        self.assertEqual(gate_status(check.g04_i_we_ratio(body)), "FAIL")


class G05SlopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = check.load_words()
        cls.patterns = check.load_patterns()

    def _g05(self, body):
        return check.g05_slop(body, self.words, self.patterns)

    def test_word_slop_fails(self):
        result = self._g05("You can leverage this data to flag players.")
        self.assertEqual(gate_status(result), "FAIL")
        self.assertTrue(result.get("hits"))

    def test_pattern_slop_fails(self):
        result = self._g05("It's not just a tool, it's a system.")
        self.assertEqual(gate_status(result), "FAIL")
        self.assertTrue(any(h["tier"] == "pattern" for h in result.get("hits", [])))

    def test_clean_passes(self):
        result = self._g05("I built a small tool to track my reading.")
        self.assertEqual(gate_status(result), "PASS")

    def test_world_of_boundary_no_false_positive(self):
        """Calibration finding 3: 'what can the world offer me?' must NOT flag."""
        result = self._g05("What can the world offer me?")
        self.assertEqual(gate_status(result), "PASS")

    def test_multiword_phrase_flags(self):
        result = self._g05("The world of data engineering is vast.")
        self.assertEqual(gate_status(result), "FAIL")


class SlopLevelTests(unittest.TestCase):
    """Level contract: fail patterns stay at zero hits on the corpus, warn patterns report without failing."""

    def setUp(self):
        self.words = check.load_words()
        self.patterns = check.load_patterns()

    def test_fail_level_stays_clean_on_the_corpus(self):
        patterns = [p for p in self.patterns if p[2] == "fail"]
        posts = sorted((REPO / "corpus").glob("*.md"))
        self.assertEqual(len(posts), 26, "corpus changed; recalibrate the fail level before touching this test")
        for path in posts:
            _meta, body = check.parse(str(path))
            text = check.prose(body)
            for rx, label, _level in patterns:
                self.assertIsNone(rx.search(text), f"{path.name} fires {label}")

    def test_two_beat_reversal_fails(self):
        result = check.g05_slop("My setup is not a toolchain. It is a way of working.", self.words, self.patterns)
        self.assertEqual(gate_status(result), check.FAIL)

    def test_comma_not_tail_warns_without_failing(self):
        result = check.g05_slop("I write for data people, not for recruiters.", self.words, self.patterns)
        self.assertEqual(gate_status(result), check.WARN)
        self.assertEqual(result["hits"][-1]["level"], "warn")

    def test_loader_reads_level_markers_and_defaults_to_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "patterns.txt"
            path.write_text("alpha\tlabel-one\n# level: warn\nbeta\tlabel-two\n", encoding="utf-8")
            levels = [(label, level) for _rx, label, level in check.load_patterns(path)]
        self.assertEqual(levels, [("label-one", "fail"), ("label-two", "warn")])


class G06StandaloneTests(unittest.TestCase):
    def test_series_opener_fails(self):
        body = "In my last post, I shared the big picture.\n\nToday I continue."
        self.assertEqual(gate_status(check.g06_standalone(body)), "FAIL")

    def test_clean_passes(self):
        body = "I built a dashboard this week.\n\nHere is how."
        self.assertEqual(gate_status(check.g06_standalone(body)), "PASS")


class G07ImageSlotsTests(unittest.TestCase):
    def test_builds_without_slots_warns(self):
        self.assertEqual(gate_status(check.g07_image_slots("Body, no images.", "builds")), "WARN")

    def test_builds_with_slots_infos_or_passes(self):
        body = "[SCREENSHOT: dashboard]\n\n[SCREENSHOT: pipeline]\n\n[SCREENSHOT: results]"
        self.assertNotEqual(gate_status(check.g07_image_slots(body, "builds")), "FAIL")


class G08FrontmatterTests(unittest.TestCase):
    def test_missing_keys_fail(self):
        result = check.g08_frontmatter({})
        self.assertEqual(gate_status(result), "FAIL")

    def test_bad_bucket_fails(self):
        meta = {"title": "x", "bucket": "not-a-bucket", "status": "checked"}
        self.assertEqual(gate_status(check.g08_frontmatter(meta)), "FAIL")

    def test_valid_passes(self):
        meta = {"title": "x", "bucket": "field-notes", "status": "checked"}
        self.assertEqual(gate_status(check.g08_frontmatter(meta)), "PASS")

    def test_explainers_bucket_passes(self):
        meta = {"title": "x", "bucket": "explainers", "status": "checked"}
        self.assertEqual(gate_status(check.g08_frontmatter(meta)), "PASS")


class RunGatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = check.load_words()
        cls.patterns = check.load_patterns()

    def test_known_good_draft_has_no_fail(self):
        """A clean field-note draft must produce zero FAIL gates (WARN is fine)."""
        meta = {"title": "Test Post", "bucket": "field-notes", "status": "checked"}
        body = (
            "I built a small tool to track my reading.\n\n"
            "It takes a list of links and turns it into a weekly digest.\n\n"
            "Here is what I learned.\n\n"
            "## How it works\n\n"
            "The tool reads a markdown file. Then it fetches each link.\n\n"
            "## What's next\n\n"
            "I want to add search next.\n\n"
            "Till next time, Ricardo."
        )
        gates = check.run_gates(meta, body, self.words, self.patterns)
        failed = [g["id"] for g in gates if g["status"] == "FAIL"]
        self.assertEqual(failed, [], f"unexpected failures: {failed}")


class StatsTests(unittest.TestCase):
    def test_one_sentence_paragraphs_counted(self):
        body = "One.\n\nTwo words.\n\nThis is a longer sentence. Here is another one."
        st = check.stats(body)
        self.assertEqual(st["one_sentence_paras"], 2)

    def test_em_dashes_and_semicolons_measured(self):
        body = "A dash — here; and a semicolon here."
        st = check.stats(body)
        self.assertEqual(st["em_dashes"], 1)
        self.assertEqual(st["semicolons"], 1)


if __name__ == "__main__":
    unittest.main()
