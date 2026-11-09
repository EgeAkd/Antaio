import tempfile
import unittest
from pathlib import Path
from antaio import plan, apply

class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_preview_does_not_change_files(self):
        (self.root / 'photo.JPG').write_bytes(b'photo')
        moves = plan(self.root)
        self.assertEqual(moves[0][1], self.root / 'Images/photo.JPG')
        self.assertTrue((self.root / 'photo.JPG').exists())
        self.assertFalse((self.root / 'Images').exists())

    def test_collision_keeps_both_contents(self):
        (self.root / 'Documents').mkdir()
        (self.root / 'Documents/note.txt').write_text('old')
        (self.root / 'note.txt').write_text('new')
        apply(plan(self.root))
        self.assertEqual((self.root / 'Documents/note.txt').read_text(), 'old')
        self.assertEqual((self.root / 'Documents/note (1).txt').read_text(), 'new')

    def test_skips_hidden_directories_and_links(self):
        (self.root / '.secret').write_text('hidden')
        (self.root / 'folder').mkdir()
        (self.root / 'link.txt').symlink_to(self.root / '.secret')
        self.assertEqual(plan(self.root), [])

    def test_rejects_symlink_destination(self):
        (self.root / 'elsewhere').mkdir()
        (self.root / 'Images').symlink_to(self.root / 'elsewhere', target_is_directory=True)
        (self.root / 'a.png').write_bytes(b'a')
        with self.assertRaises(ValueError):
            plan(self.root)

    def test_late_collision_is_not_overwritten(self):
        (self.root / 'a.txt').write_text('new')
        moves = plan(self.root)
        (self.root / 'Documents').mkdir()
        (self.root / 'Documents/a.txt').write_text('existing')
        with self.assertRaises(FileExistsError):
            apply(moves)
        self.assertEqual((self.root / 'a.txt').read_text(), 'new')
        self.assertEqual((self.root / 'Documents/a.txt').read_text(), 'existing')

if __name__ == '__main__':
    unittest.main()
