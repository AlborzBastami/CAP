# split_xml_chunks.py
from lxml import etree

path1 = "e:\\OneDrive\\MHH\\Eigene Dateien MHH\\CAP Studie\\GitHub CAP\\CAP\\Alt\\proj_PROJ2_Dev_20250705-1958_Cereb_Flui_Analy_in_Psych_CAP_.xml"
path2 = "e:\\OneDrive\\MHH\\Eigene Dateien MHH\\CAP Studie\\GitHub CAP\\CAP\\Ziel\\proj_CAP_Dev_20250705-2314_Cereb_Flui_Analy_in_Psych_CAP.xml"


def chunk_xml(input_path: str, prefix: str,
              root_tag: str, record_tag: str,
              chunk_size: int = 200000):
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
    chunk_xml(path1, "file1_chunk", "root", "item")
    chunk_xml(path2, "file2_chunk", "root", "item")