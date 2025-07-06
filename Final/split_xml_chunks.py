# split_xml_chunks.py
from lxml import etree

def chunk_xml(input_path: str, prefix: str,
              root_tag: str, record_tag: str,
              chunk_size: int = 10000):
    """
    Liest input_path mit iterparse zeilenweise
    und schreibt validierte Teil-XMLs mit je chunk_size records:
      prefix_1.xml, prefix_2.xml, …
    """
    header = f'<?xml version="1.0" encoding="UTF-8"?>\n<{root_tag}>\n'.encode()
    footer = f'</{root_tag}>\n'.encode()

    context = etree.iterparse(input_path, events=('end',), tag=record_tag, huge_tree=True)
    part, count, out = 1, 0, None
    for _, elem in context:
        if count % chunk_size == 0:
            if out:
                out.write(footer); out.close()
            out = open(f'{prefix}_{part}.xml','wb')
            out.write(header); part += 1
        out.write(etree.tostring(elem, pretty_print=True))
        # Speicher freigeben
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        count += 1
    if out:
        out.write(footer); out.close()

if __name__ == "__main__":
    # Beispielaufruf
    chunk_xml("file1.xml", "file1_chunk", "root", "item")
    chunk_xml("file2.xml", "file2_chunk", "root", "item")
# split_xml_chunks.py