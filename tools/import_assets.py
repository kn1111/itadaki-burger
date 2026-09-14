"""ゲームのリポジトリから画像とフォントのライセンスを取り込む。既にあるファイルは上書きしない (--force で上書き)。

  python tools/import_assets.py [--force]

- ja / en のスクリーンショット: docs/store/screenshots/current/{ja,en}_*.png (2560x1440) を最近傍で 1/2
- 他の言語: docs/store/screenshots/<prefix>_*.png (1920x1080) をそのまま
- ロゴ: build/capsules/library_logo_1280x720_<steam>.png の透過部分を切り詰め
- OGP: build/capsules/header_920x430_<steam>.png
"""
import os
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BURGER = os.environ.get("BURGER", "C:/Users/knoza/burger")
FORCE = "--force" in sys.argv

# サイトの接頭辞 → (Steam の言語名, スクショの接頭辞, スクショの並び)
CURRENT = ["1_title", "2_run", "3_score", "4_result", "5_shop"]
LOCAL = ["1_title", "3_run", "4_result", "5_shop", "6_codex"]
SPEC = {
    "ja": ("japanese", "current/ja", CURRENT),
    "en": ("english", "current/en", CURRENT),
    "zh-hans": ("schinese", "zh", LOCAL),
    "zh-hant": ("tchinese", "zht", LOCAL),
    "ko": ("koreana", "ko", LOCAL),
    "de": ("german", "de", LOCAL),
    "fr": ("french", "fr", LOCAL),
    "es": ("latam", "es", LOCAL),
    "pt-br": ("brazilian", "pt", LOCAL),
    "ru": ("russian", "ru", LOCAL),
}


def want(dst):
    if os.path.exists(dst) and not FORCE:
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    return True


def main():
    for code, (steam, prefix, shots) in SPEC.items():
        for i, name in enumerate(shots, 1):
            src = "%s/docs/store/screenshots/%s_%s.png" % (BURGER, prefix, name)
            dst = "%s/assets/ss/%s-%d.png" % (ROOT, code, i)
            if not want(dst):
                continue
            im = Image.open(src)
            if im.width == 2560:
                im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)
            im.save(dst, optimize=True)
            print("ss  ", dst, im.size)
        dst = "%s/assets/logo-%s.png" % (ROOT, code)
        if want(dst):
            im = Image.open("%s/build/capsules/library_logo_1280x720_%s.png" % (BURGER, steam)).convert("RGBA")
            x0, y0, x1, y1 = im.getchannel("A").getbbox()
            p = 8
            im.crop((max(0, x0 - p), max(0, y0 - p), min(im.width, x1 + p), min(im.height, y1 + p))).save(dst, optimize=True)
            print("logo", dst)
        dst = "%s/assets/og-%s.png" % (ROOT, code)
        if want(dst):
            shutil.copy("%s/build/capsules/header_920x430_%s.png" % (BURGER, steam), dst)
            print("og  ", dst)

    fusion = ROOT + "/fonts/fusion-pixel"
    if want(fusion + "/OFL.txt"):
        shutil.copy(BURGER + "/assets/fonts/fusion-pixel/OFL.txt", fusion + "/OFL.txt")
        shutil.copytree(BURGER + "/assets/fonts/fusion-pixel/LICENSES", fusion + "/LICENSES", dirs_exist_ok=True)
        print("license", fusion)


if __name__ == "__main__":
    main()
