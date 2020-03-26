# zefania-bible-2-verseview7x
Convert Zefania Bible 2 VerseView 7x bible format

VerseView 7x moved away from Zefania XML format for Bible. Now it uses SQLite db.

## Steps for converting **NKJV** Zefania XML Bible to VerseView 7x Bible format:

1. Get your required Bible Translation in Zefania XML Bible format. Eg: `nkjv.xml`
2. Run `Zefania2VerseView7x.py --xml-bile <xml file path>`.
  This will convert XML Bible into CSV format with same filename with added extension `.csv`
3. Download [kjv](http://www.verseview.info/download/bibledb/kjv.db) from VerseView.
4. Open kjv.db in `sqlite3` and run as following:
```
sqlite3 ./kjv.db
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> delete from words;
sqlite> .mode csv
sqlite> .import nkjv.xml.csv words
```
5. Rename `kjv.db` to `nkjv.db`
6. Import `nkjv.db` into VerseView 7x using `Add Bible`


