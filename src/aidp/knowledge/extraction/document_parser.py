import os
from collections.abc import Iterator

import fitz  # type: ignore[import-untyped]

from aidp.knowledge.serialization import Provenance


class DocumentParser:
    """
    Parses PDF documents into text blocks with provenance tracking.
    """
    
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        
    def parse_blocks(self) -> Iterator[tuple[str, Provenance]]:
        """
        Yields (text_block, Provenance) for each block in the document.
        """
        doc = fitz.open(self.file_path)
        doc_id = f"file://{os.path.basename(self.file_path)}"
        
        for page_num, page in enumerate(doc):
            blocks = page.get_text("blocks")
            for chunk_idx, block in enumerate(blocks):
                # block is a tuple, typically (x0, y0, x1, y1, text, block_no, block_type)
                text = block[4].strip()
                if not text:
                    continue
                    
                prov = Provenance(
                    document_id=doc_id,
                    page_number=page_num + 1,
                    paragraph_id=f"p_{chunk_idx}",
                    offset_start=0,
                    offset_end=len(text),
                    chunk_index=chunk_idx
                )
                yield text, prov
                
        doc.close()
