# sdvx-romanizer

Generates a SOUND VOLTEX music_db.xml with Japanese titles translated to their
romanized version, using RemyWiki page titles as a reference.

## Requirements

- Requests https://pypi.org/project/requests/

## Usage

This will create `data_mods/romanized_titles/others/music_db.xml` using the
`music_db.xml` file in the current working directory as a base:

```
python create_translated_db.py
```


You can specify an input and output path for `music_db.xml`

```
python create_translated_db.py input_music_db.xml output_music_db.xml
```


You can perform a dry run that will tell you which titles would be looked up on
RemyWiki, without performing actual requests, this shows you all missing
translations

```
python create_translated_db.py --check

> Not looking up untranslated title: 「ここなつ☆」は夢のカタチ title_clean='ここなつは夢のカタチ' display_title='「ここなつ☆」は夢のカタチ'
```


Instead of replacing titles with the romanized version, you can include both.
For example "神威" would become "神威 / Kamui".

```
python create_translated_db.py --both
```

## How to use the generated file

Either replace the original file, or use [ifs_layeredfs](https://github.com/mon/ifs_layeredfs)


## License

MIT.
