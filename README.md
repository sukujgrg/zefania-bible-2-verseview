[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

# Zefania XML Bible to [VerseView](http://verseview.info/vv/)
Convert Zefania Bible to [VerseView](http://verseview.info/vv/) bible format

Since [VerseView](http://verseview.info/vv/)>=7x moved away from Zefania XML bible format. Now it uses SQLite db.

## To convert
Pass the xml to the script as argument and it will create the sqlite db file in the same path with `.db` as suffix.

    % python3 Zefania2VerseView.py /tmp/Bible_English_NKJV.xml
    /tmp/Bible_English_NKJV.xml -> /tmp/Bible_English_NKJV.db

Notes:
---
- Some Zefania XML files we can see around doesn't contain `bname` attribute for each books.
Such XML files won't work with this script wihout modification.
