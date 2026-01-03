import json
from argparse import ArgumentParser
from pathlib import Path

import requests


# from https://stackoverflow.com/a/37311125
def is_cjk(character):
    """ "
    Checks whether character is CJK.

        >>> is_cjk(u'\u33fe')
        True
        >>> is_cjk(u'\ufe5f')
        False

    :param character: The character that needs to be checked.
    :type character: char
    :return: bool
    """
    return any(
        [
            start <= ord(character) <= end
            for start, end in [
                (4352, 4607),
                (11904, 42191),
                (43072, 43135),
                (44032, 55215),
                (63744, 64255),
                (65072, 65103),
                (65381, 65500),
                (131072, 196607),
            ]
        ]
    )


CACHE_FILE = Path("translated_titles_cache.json")

# special characters used by the game to insert accented letters etc
# from https://github.com/FairyJoke/fairyjoke-legacy/blob/master/database/scripts/import_sdvx_data.py
SPECIAL_CHARS_TRANSLATION_TABLE = {
    "龕": "€",
    "釁": "🍄",
    "驩": "Ø",
    "曦": "à",
    "齷": "é",
    "骭": "ü",
    "齶": "♡",
    "彜": "ū",
    "罇": "ê",
    "雋": "Ǜ",
    "鬻": "♃",
    "鬥": "Ã",
    "鬆": "Ý",
    "曩": "è",
    "驫": "ā",
    "躔": "★",
    "齲": "♥",
    "騫": "á",
    "趁": "Ǣ",
    "鬮": "¡",
    "盥": "⚙︎",
    "隍": "︎Ü",
    "頽": "ä",
    "餮": "Ƶ",
    "黻": "*",
    "蔕": "ũ",
    "闃": "Ā",
    "饌": "²",
    "煢": "ø",
    "鑷": "ゔ",
    "=墸Σ": "=͟͟͞ Σ",
    "鹹": "Ĥ",
    "瀑i": "Ài",
    "疉": "Ö",
    "鑒": "₩",
    "Ryu??": "Ryu☆",
}

remywiki_converted_chars = {
    "煉": "練",
    "&amp;": "&",
}

MANUAL_TRANSLATIONS = {
    "ませまてぃっく齲ま+ま=まじっく！": "Mathematic ma+ma=magic!",
    "「ここなつ☆」は夢のカタチ": '"Coconatsu" wa yume no katachi',
    "雪月花 (Shiron &amp; Sound Artz Remix)": "Setsugekka (Shiron & Sound Artz Remix)",
    "トーホータノシ (feat. 抹)": "Touhou tanoshi feat. Matsu",
    "セイレーン ～悲壮の竪琴～": "Siren ~hisou no tategoto~",
    "おーとめーしょんぱらだいす": "AUTOMATION PARADISE",
    "うぇるかむ -||祭みっくす||-": "VVelcome -matsuri mix-",
    "ユニバーページ（i-world Mix）": "Univer page (i-world Mix)",
    "かくしん的☆めたまるふぉ～ぜっ！（crabMixx）": "Kakushinteki metamaruphose! (crabMixx)",
    "鏡面の波（ramble mix）": "Kyoumen no nami (ramble mix)",
    "ふ・れ・ん・ど・し・た・い（WEREHEREMIX)": "Friend shitai (WEREHEREMIX)",
    "WobbleTangleFestival (影虎。 &amp; ikaruga_nex's HDM RMX)": "WobbleTangleFestival (Kagetora. & ikaruga nex's HDM RMX)",
    "Redo／アニメ「Re:ゼロから始める異世界生活」より": "Redo (from Re:Zero)",
    "Realize／アニメ「Re:ゼロから始める異世界生活」より": "Realize (from Re:Zero)",
    "忘れないように、失くさないように": "Wasurenai youni, nakusanai youni",
    "Growing Up／アニメ「この素晴らしい世界に祝福を！３」より": "Growing Up (from KonoSuba S3)",
    "B.B.K.K.B.K.K. (影虎。 &amp; siqlo PsyRemix)": "B.B.K.K.B.K.K. (Kagetora. & siqlo PsyRemix)",
}

parser = ArgumentParser()
parser.add_argument(
    "path_to_music_db", default="music_db.xml", type=Path, nargs="?"
)
parser.add_argument(
    "output_path",
    default="data_mods/romanized_titles/others/music_db.xml",
    type=Path,
    nargs="?",
)
parser.add_argument(
    "--check",
    action="store_true",
    help=(
        "Check for untranslated titles, without querying remywiki for"
        " translations"
    ),
)
args = parser.parse_args()

if CACHE_FILE.exists():
    with CACHE_FILE.open() as f:
        translations = json.load(f)
else:
    translations = {}

translations.update(MANUAL_TRANSLATIONS)

args.output_path.parent.mkdir(exist_ok=True, parents=True)


def get_translated_title_from_remywiki(title):
    response = requests.get(
        f"https://remywiki.com/index.php?search={title}", timeout=30
    )
    response.raise_for_status()
    for line in response.text.splitlines():
        if line.strip().startswith("<title>"):
            start = line.find("<title>") + len("<title>")
            end = line.find("</title>")
            page_title = line[start:end]
            if page_title.startswith("Search results for "):
                print(
                    "RemyWiki redirected to search results, ambigous title?",
                    title,
                )
                return None
            end = page_title.find(" - RemyWiki")
            if end == -1:
                print(
                    "Title does not look like a RemyWiki page title:",
                    page_title,
                )
                return None

            translated_title = page_title[:end]
            return translated_title
    return None


with args.path_to_music_db.open(encoding="cp932") as input_file:
    with args.output_path.open("w", encoding="cp932") as output_file:
        for line in input_file:
            if not line.strip().startswith("<title_name>"):
                output_file.write(line)
                continue

            start = line.find("<title_name>") + len("<title_name>")
            end = line.find("</title_name>")
            title = line[start:end]

            if title not in translations:
                title_clean = title
                for old, new in SPECIAL_CHARS_TRANSLATION_TABLE.items():
                    title_clean = title_clean.replace(old, new)

                for old, new in remywiki_converted_chars.items():
                    title_clean = title_clean.replace(old, new)

                display_title = title_clean

                common_special_chars = (
                    " .'\"*-!?↓()/_“”#[]∞α∠~☆&;★,～$+△！×↑:？＊=※{}’÷：◆†…←→"
                    "＋＝♪∴∵《Δ》∽σЯθ凸Ψ。°゜ΣΛ⑨・（）･∀「」H、　Ø≡｡ﾟ｡"
                    # "齷驩瀑鬮頽鹹闃饌煢蔕盥齶罇曦龕隍彜雋鬻鬆鬥曩驫趁齲骭"
                )
                title_clean = "".join(
                    char
                    for char in title_clean
                    if char not in common_special_chars
                )
                if any(is_cjk(char) for char in title_clean):
                    if args.check:
                        print(
                            "Not looking up untranslated title:",
                            title,
                            f"{title_clean=} {display_title=}",
                        )
                    else:
                        print("Looking up", display_title, "on RemyWiki")
                        remywiki_title = get_translated_title_from_remywiki(
                            display_title
                        )
                        if not remywiki_title:
                            print(
                                "No translation found for", title, "skipping..."
                            )
                        else:
                            translations[title] = remywiki_title
                            with CACHE_FILE.open("w") as f:
                                json.dump(translations, f, indent=2)

            translated_title = translations.get(title, title)
            for old, new in SPECIAL_CHARS_TRANSLATION_TABLE.items():
                translated_title = translated_title.replace(new, old)
            translated_title = translated_title.replace("&amp;", "&")
            translated_title = translated_title.replace("&", "&amp;")
            translated_line = line[:start] + translated_title + line[end:]
            try:
                output_file.write(translated_line)
            except UnicodeEncodeError as e:
                print("UnicodeEncodeError while writing line:", translated_line)
                raise e
