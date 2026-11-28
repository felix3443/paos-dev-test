import base64
import binascii
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# Pinned from the implementation-time authentication run against real git
# history. These prove consistency with that evidence, not independent
# historical authenticity.
EVIDENCE_SHA256 = "99be17269d630a221480d2cf293c938c488b8f1e4d4d4c6ed7249670a4203c41"
BASELINE_SHA256 = "19f16d476c82cc850bbeb5c79ab37096615770fea5b11f6b85785932a47304fa"
MERGED_SHA256 = "8eecbdaa2221871809fd2e664ed6e888166a57ddc2e4690a75bb5df399510773"
PARENT = "cdae182637988f68089ea332fceda735e1c3a587"
MERGE = "8478b37266252f1adef561e72e4aec548782cc7c"
OLD_HEADING = b"# paos-dev-test"
NEW_HEADING = b"# superagent-dev-test"
BASE_BLOB = "6d96a1d560f5254be083fd96c429b080361c09c2"
MERGED_BLOB = "6d42e57f7ed87b94793a638ab05432b88445cadf"
EXPECTED_PATCH = (
    "diff --git a/README.md b/README.md\n"
    f"index {BASE_BLOB}..{MERGED_BLOB} 100644\n"
    "--- a/README.md\n"
    "+++ b/README.md\n"
    "@@ -1,4 +1,4 @@\n"
    "-# paos-dev-test\n"
    "+# superagent-dev-test\n"
    " \n"
    " Toy Python package used to test an automated development loop. Run tests with `python -m unittest discover -s tests -v`.\n"
    " \n"
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def decode_baseline(text):
    return base64.b64decode(text.strip(), validate=True)


def parse_manifest(text):
    entries = {}
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, blob = meta.split(" ")
        if kind != "blob" or path in entries:
            raise ValueError(f"bad manifest line: {line!r}")
        entries[path] = (mode, blob)
    return entries


def check_patch(patch, parent_tree, merge_tree):
    if patch != EXPECTED_PATCH:
        raise ValueError("patch differs from pinned historical patch")
    mode = "100644"
    if parent_tree["README.md"] != (mode, BASE_BLOB):
        raise ValueError("parent manifest README entry disagrees with patch")
    if merge_tree["README.md"] != (mode, MERGED_BLOB):
        raise ValueError("merge manifest README entry disagrees with patch")


def check_manifests(parent_tree, merge_tree):
    if set(parent_tree) != set(merge_tree):
        raise ValueError("file sets differ")
    differing = sorted(p for p in parent_tree if parent_tree[p] != merge_tree[p])
    if differing != ["README.md"]:
        raise ValueError(f"unexpected differing paths: {differing}")
    if parent_tree["README.md"][0] != merge_tree["README.md"][0]:
        raise ValueError("README mode changed")


def reconstruct_merged(baseline):
    first, sep, rest = baseline.partition(b"\n")
    if first != OLD_HEADING or not sep:
        raise ValueError("baseline heading is not the original heading")
    merged = NEW_HEADING + b"\n" + rest
    if sha256(merged) != MERGED_SHA256:
        raise ValueError("reconstructed merged README digest mismatch")
    return merged


def check_live_heading(readme):
    if readme.partition(b"\n")[0] != NEW_HEADING:
        raise ValueError("live README heading is not the renamed heading")


class Readme77EvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (FIXTURES / "readme_77_evidence.json").read_bytes()
        cls.evidence_raw = raw
        cls.evidence = json.loads(raw)
        cls.baseline_text = (FIXTURES / "readme_77_base.b64").read_text()
        cls.baseline = decode_baseline(cls.baseline_text)
        cls.parent_tree = parse_manifest(cls.evidence["tree_parent"])
        cls.merge_tree = parse_manifest(cls.evidence["tree_merge"])

    def test_fixture_digests_pinned(self):
        self.assertEqual(sha256(self.evidence_raw), EVIDENCE_SHA256)
        self.assertEqual(sha256(self.baseline), BASELINE_SHA256)
        self.assertEqual(len(self.baseline), 1676)

    def test_evidence_metadata(self):
        ev = self.evidence
        self.assertEqual(ev["parent"], PARENT)
        self.assertEqual(ev["merge"], MERGE)
        self.assertEqual(ev["changed_paths"], ["README.md"])
        self.assertEqual(ev["baseline_readme"], {"length": 1676, "sha256": BASELINE_SHA256, "first_line": "# paos-dev-test"})
        self.assertEqual(ev["merged_readme"], {"length": 1682, "sha256": MERGED_SHA256, "first_line": "# superagent-dev-test"})
        self.assertTrue(ev["remainder_equal"])
        self.assertTrue(ev["live_readme_equals_merged"])
        self.assertTrue(ev["commands"])

    def test_strict_base64_decoding(self):
        with self.assertRaises(binascii.Error):
            decode_baseline(self.baseline_text.strip() + "!")

    def test_patch_matches_manifests(self):
        check_patch(self.evidence["full_index_patch"], self.parent_tree, self.merge_tree)

    def test_manifests_differ_only_in_readme(self):
        check_manifests(self.parent_tree, self.merge_tree)

    def test_reconstruction_preserves_remainder(self):
        merged = reconstruct_merged(self.baseline)
        self.assertEqual(len(merged), 1682)
        self.assertEqual(merged.partition(b"\n")[2], self.baseline.partition(b"\n")[2])

    def test_live_readme_heading(self):
        check_live_heading((ROOT / "README.md").read_bytes())

    def test_rejects_wrong_heading(self):
        with self.assertRaises(ValueError):
            reconstruct_merged(b"# other" + self.baseline[len(OLD_HEADING):])
        with self.assertRaises(ValueError):
            check_live_heading(b"# paos-dev-test\nrest\n")

    def test_rejects_remainder_mutation(self):
        mutated = self.baseline[:-2] + b"X\n"
        with self.assertRaises(ValueError):
            reconstruct_merged(mutated)

    def test_rejects_patch_tampering(self):
        patch = self.evidence["full_index_patch"]
        tampered = [
            patch + "diff --git a/x b/x\n",
            patch + "@@ -9,1 +9,1 @@\n-a\n+b\n",
            patch.replace("100644", "100755"),
            patch.replace(BASE_BLOB, "0" * 40),
        ]
        for t in tampered:
            with self.subTest(t=t[-30:]), self.assertRaises(ValueError):
                check_patch(t, self.parent_tree, self.merge_tree)
        bad_tree = dict(self.merge_tree, **{"README.md": ("100644", "1" * 40)})
        with self.assertRaises(ValueError):
            check_patch(patch, self.parent_tree, bad_tree)

    def test_rejects_manifest_tampering(self):
        cases = [
            dict(self.merge_tree, **{"web/index.html": ("100644", "2" * 40)}),
            dict(self.merge_tree, **{"extra.txt": ("100644", "3" * 40)}),
            {p: v for p, v in self.merge_tree.items() if p != ".gitignore"},
            dict(self.merge_tree, **{"README.md": ("100755", MERGED_BLOB)}),
        ]
        for c in cases:
            with self.subTest(), self.assertRaises(ValueError):
                check_manifests(self.parent_tree, c)

    def test_allows_future_readme_additions(self):
        merged = reconstruct_merged(self.baseline)
        check_live_heading(merged + b"\n## New section\n\nMore docs.\n")


if __name__ == "__main__":
    unittest.main()
