import argparse
import sqlite3
import sys

from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET


class CreateVVDb:

    BOOK_NAME = "bname"
    BOOK_NUMBER = "bnumber"
    CHAPTER = "cnumber"
    VERSE = "vnumber"

    def __init__(self, xml_path: Path):
        self.xml_path: str = str(xml_path)
        self.db_path = xml_path.with_suffix(".db")

    def check_db_exists(self):
        if self.db_path.exists():
            prompt = input(f"{self.db_path} exists. Should I delete? [Y/n]")
            if prompt.lower().startswith("n"):
                sys.exit(0)
            elif prompt.lower().startswith("y") or not prompt.strip():
                self.db_path.unlink()
            else:
                sys.exit(1)

    def path(self):
        print(f"{self.xml_path} -> {self.db_path}")

    def words(self, data: List[List]):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        words_sql = """
                        CREATE TABLE IF NOT EXISTS `words` (
                            `wordId`    INTEGER PRIMARY KEY AUTOINCREMENT,
                            `word`      TEXT,
                            `bookNum`   INTEGER,
                            `chNum`     INTEGER,
                            `verseNum`  INTEGER
                        );
                    """
        c.execute(words_sql)
        c.executemany("""INSERT INTO words VALUES (?,?,?,?,?)""", data)
        conn.commit()

    def conf(self, books: List):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        configuration_sql = """
                            CREATE TABLE IF NOT EXISTS `configuration` (
                                `revision`      INTEGER,
                                `fonts`         TEXT,
                                `booknames`     TEXT,
                                `title`         TEXT,
                                `description`   TEXT,
                                `copyrights`    TEXT,
                                `sizefactor`    INTEGER
                            );
                        """
        c.execute(configuration_sql)
        db_stem = self.db_path.stem
        data = [1, "", ",".join(books), db_stem, db_stem, db_stem, 0]
        c.execute("""INSERT INTO configuration VALUES (?,?,?,?,?,?,?)""", data)
        c.execute(configuration_sql)
        conn.commit()

    def export_xml(self) -> Tuple[List[List], List[str]]:
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        word_id = 0
        book_num = 0
        words = []
        books = []
        for book in root:
            book_num += 1
            books.append(book.attrib[self.BOOK_NAME])
            for chapter in book:
                for verse in chapter:
                    word_id += 1
                    words.append(
                        [
                            word_id,
                            verse.text.strip(),
                            int(book.attrib[self.BOOK_NUMBER]),
                            int(chapter.attrib[self.CHAPTER]),
                            int(verse.attrib[self.VERSE]),
                        ]
                    )

        return words, books


def main(xml_path):
    xml_path = Path(xml_path.name)
    try:
        vv = CreateVVDb(xml_path)
        words, books = vv.export_xml()
        vv.check_db_exists()
        vv.words(words)
        vv.conf(books)
        vv.path()
    except Exception as e:
        raise (e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export Zefania XML Bible to VerseView 7.x/8.x Bible format."
    )
    parser.add_argument("xml_bible", type=argparse.FileType("r", encoding="UTF-8"))

    args = parser.parse_args()
    main(args.xml_bible)
