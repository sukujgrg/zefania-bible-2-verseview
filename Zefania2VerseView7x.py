import csv

from pathlib import Path
import xml.etree.ElementTree as ET

import argparse

def export_xml_to_csv(xml_bible):
    tree = ET.parse(xml_bible.name)
    root = tree.getroot()
    wordId = 0
    bookNum = 0
    rows = []

    for book in root:
        if not book.attrib.get("n"):
            continue
        bookNum += 1    
        for chapter in book:
            for verse in chapter:
                wordId += 1
                rows.append([wordId, verse.text, bookNum, chapter.attrib['n'], verse.attrib['n']])

    csv_filename = xml_bible.name + '.csv'
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
    print("Expoted to " + csv_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export Zefania XML Bible to VerseView 7.x Bible format.')
    parser.add_argument('--xml-bible', type=argparse.FileType('r', encoding='UTF-8'), required=True)

    args = parser.parse_args()
    export_xml_to_csv(args.xml_bible)