# sdvx-romanizer

Generates a SOUND VOLTEX music_db.xml with Japanese titles translated to their
romanized version, using RemyWiki page titles as a reference.

## Requirements

- Requests https://pypi.org/project/requests/

## Usage

Create `data_mods/romanized_titles/others/music_db.xml` by using the
`music_db.xml` in the current directory as a base.

```
python create_translated_db.py
```


Specify path for base `music_db.xml`

```
python create_translated_db.py games/sdvx/konaste/unpacked/data/others/music_db.xml
```


Check which titles will be looked up on RemyWiki, without performing actual
requests

```
python create_translated_db.py --check
```


Instead of replacing titles with the romanized version, include both, for
example: "神威 / Kamui"

```
python create_translated_db.py --both
```


Display all help

```
python create_translated_db.py --help
```

## How to use the generated file

Either replace the original file, or use [ifs_layeredfs](https://github.com/mon/ifs_layeredfs)


## License

MIT.
