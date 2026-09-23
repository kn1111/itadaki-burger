"""ゲームのリポジトリから画像とフォントのライセンスを取り込む。既にあるファイルは上書きしない (--force で上書き)。

  python tools/import_assets.py [--force]

- スクリーンショット: build/store/<prefix>_*.png (1920x1080、Steam のストアと同じもの) をそのまま
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

# サイトの接頭辞 → (Steam の言語名, スクショの接頭辞)
# 2026-09-23: スクショはゲーム側の build/store (tools/store_shots.ps1 の出力 = Steam のストアに上げているのと
# 同じ 1920x1080) から取る。以前は docs/store/screenshots/ の古い置き場から、日英だけ別選定の 5 枚
# (2560px の 1/2) を取っていて、ストアを撮り直しても古い客・古い店主のままだった。並びも全言語で揃える
SHOTS = ["1_title", "3_run", "4_result", "5_shop", "6_codex"]
SPEC = {
    "ja": ("japanese", "ja"),
    "en": ("english", "en"),
    "zh-hans": ("schinese", "zh"),
    "zh-hant": ("tchinese", "zht"),
    "ko": ("koreana", "ko"),
    "de": ("german", "de"),
    "fr": ("french", "fr"),
    "es": ("latam", "es"),
    "pt-br": ("brazilian", "pt"),
    "ru": ("russian", "ru"),
}


def want(dst):
    if os.path.exists(dst) and not FORCE:
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    return True


def main():
    for code, (steam, prefix) in SPEC.items():
        for i, name in enumerate(SHOTS, 1):
            src = "%s/build/store/%s_%s.png" % (BURGER, prefix, name)
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
