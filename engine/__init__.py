"""BOS-FS Engine — Optional Python Backend."""

__version__ = "0.1.0"

# Book Knowledge Ingestor (numeric directory name requires importlib)
import importlib.util
import os as _os

_ingestor_path = _os.path.join(_os.path.dirname(__file__), "core", "07_knowledge_ingestor", "book_ingestor.py")
_ingestor_spec = importlib.util.spec_from_file_location("book_ingestor", _ingestor_path)
_ingestor_mod = importlib.util.module_from_spec(_ingestor_spec)
_ingestor_spec.loader.exec_module(_ingestor_mod)

BookIngestor = _ingestor_mod.BookIngestor
BookChapter = _ingestor_mod.BookChapter
