# いただきバーガー 公式サイト

いただきバーガー / A Bun Above (Steam App 5161560) の紹介ページ。https://kn1111.github.io/itadaki-burger/
検索エンジンが Steam ページにたどり着く入口で、Steamworks の「ゲーム ウェブサイト」欄にもこの URL を入れてある。
ゲーム本体のリポジトリ (`kn1111/burger`、非公開) とは別の公開リポジトリ。main 直下を GitHub Pages が配信する (push から 1 分ほどで反映)。

## 言語

Steam ストアの対応言語に合わせた 10 言語。

| パス | 言語 | 名前 | 見出しフォント |
|---|---|---|---|
| `/` | 日本語 | いただきバーガー | PixelMplus |
| `/en/` | English | A Bun Above | PixelMplus |
| `/zh-hans/` | 简体中文 | 顶饱汉堡 | Fusion Pixel (zh_hans) |
| `/zh-hant/` | 繁體中文 | 頂飽漢堡 | Fusion Pixel (zh_hant) |
| `/ko/` | 한국어 | 탑버거 | Fusion Pixel (ko) |
| `/de/` | Deutsch | Burger obenauf | PixelMplus |
| `/fr/` | Français | Un pain au-dessus | PixelMplus |
| `/es/` | Español | Burger a Tope | PixelMplus |
| `/pt-br/` | Português (Brasil) | Pão nas Alturas | PixelMplus |
| `/ru/` | Русский | Булка Что Надо | 普通の書体 (PixelMplus のキリル文字は全角なので、ゲームと同じく使わない) |

## 更新のしかた

**`index.html` と `sitemap.xml` と `fonts/*-subset.*` は生成物なので直接いじらない。**

1. 文言を直す: `tools/content.py` (10 言語ぶん。文章の元はゲーム側のストア説明文で、用語はそれに合わせてある)
2. 見た目を直す: `style.css` (全言語共通)、HTML の骨組みは `tools/build.py` の `render()`
3. 生成する: `python tools/build.py`
   - 全ページ・sitemap.xml を書き出し、ページで使っている字だけで見出しフォントを作り直す
   - フォントの元ファイルはゲームのリポジトリから読む (環境変数 `BURGER`、既定 `C:/Users/knoza/burger`)。
     中韓のフォントは大きいので数分かかる
4. commit して push

画像を差し替えるときは、該当ファイルを消してから `python tools/import_assets.py` (全部作り直すなら `--force`)。
取り込み元:

- スクリーンショット: ja/en は `burger/docs/store/screenshots/current/` (2560px を最近傍で 1/2)、他は `burger/docs/store/screenshots/<prefix>_*.png` (1920px のまま)
- ロゴ: `burger/build/capsules/library_logo_1280x720_<steam言語>.png` の透過部分を切り詰め
- OGP: `burger/build/capsules/header_920x430_<steam言語>.png`
- 歯車: `nozworks-brand/png/nozworks_gear_128.png`

## 置いてあるもの

| パス | 内容 |
|---|---|
| `google145ac5b1327006cd.html` | **Google Search Console の所有確認ファイル。消すと確認が外れる** |
| `robots.txt` / `sitemap.xml` | 検索エンジン向け (sitemap は全言語の hreflang 付き) |
| `fonts/` | 見出しフォントのサブセット + ライセンス (PixelMplus: M+ FONT LICENSE、Fusion Pixel: SIL OFL 1.1) |
| `.nojekyll` | GitHub Pages で Jekyll 処理を通さない |

## 後で入れるもの (render() にコメントで枠がある)

- 予告編: YouTube に上げたら `#about` の iframe を有効にする
- 体験版: Next フェス (2026年10月) で公開されたら `#demo` の位置に告知を足す
