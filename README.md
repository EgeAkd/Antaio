# Antaio

**A preview-first file organizer for everyday digital clutter.**

Antaio groups files into Images, Documents, Archives, Audio, Video and Other. It runs locally, uses only Python's standard library, and shows a plan before changing anything.

## Quick start

Requires Python 3.10 or newer. No packages, account or API key needed.

```sh
git clone https://github.com/EgeAkd/Antaio.git
cd Antaio
python3 antaio.py /path/to/downloads
# Review the preview, then explicitly apply:
python3 antaio.py /path/to/downloads --apply
```

```text
invoice.pdf -> Documents/invoice.pdf
photo.JPG -> Images/photo.JPG
2 file(s). Preview only. Add --apply to organize.
```

## Behavior

- Only files directly inside the selected directory are considered; subdirectories are untouched.
- Hidden files and symbolic links are skipped.
- Existing names receive a numbered suffix. Existing destination files are never overwritten.
- Applying prints a JSON record of completed moves to standard output.
- No network requests or telemetry.

**Limitations:** moving uses hard links followed by unlinking the original, so source and destination must support hard links on the same filesystem. A batch is not transactional: if a later file fails, earlier moves remain applied. Do not run while another process changes the source or destination directory. Back up important files first. There is no automatic undo.

## Development

```sh
python3 -m unittest discover -s tests -v
```

Tests cover preview behavior, collisions, hidden files, symlinks and a destination created after planning. GitHub Actions runs the suite on Linux, macOS and Windows with Python 3.10 and 3.12.

## Türkçe

Dosyaları türlerine göre klasörlere ayıran küçük bir komut satırı aracı. İlk çalıştırmada yalnızca planı gösterir; dosyaları taşımak için `--apply` eklenmelidir. Alt klasörlere girmez, gizli dosyaları ve sembolik bağlantıları atlar, aynı adlı dosyaların üzerine yazmaz.

## License

[Eclipse Public License 2.0](LICENSE), retaining this repository's original license.
