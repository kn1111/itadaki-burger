# いただきバーガー 公式サイト

いただきバーガー / A Bun Above (Steam App 5161560) の紹介ページ。
検索エンジンが Steam ページにたどり着く入口と、Steamworks の「ゲーム ウェブサイト」欄に入れる URL を兼ねる。
ゲーム本体のリポジトリ (`kn1111/burger`、非公開) とは別の**公開リポジトリ**に置く。

## 中身

| パス | 内容 |
|---|---|
| `index.html` | 日本語ページ |
| `en/index.html` | 英語ページ |
| `style.css` | 両ページ共通 |
| `assets/` | ヒーロー画像、ロゴ、スクリーンショット (ゲームの 2560px 版を最近傍で 1/2)、OGP 画像、アイコン |
| `fonts/` | PixelMplus12 を 2 ページで使う文字だけに絞ったもの + ライセンス |
| `robots.txt` / `sitemap.xml` | 検索エンジン向け |
| `.nojekyll` | GitHub Pages で Jekyll 処理を通さない |

素材の出どころ (差し替えるときはここから作り直す):

- ヒーロー: `burger/build/capsules/library_hero_3840x1240.png`
- ロゴ: `burger/build/capsules/library_logo_1280x720_{japanese,english}.png` の透過部分を切り詰め
- OGP: `burger/build/capsules/header_920x430_{japanese,english}.png`
- スクリーンショット: `burger/docs/store/screenshots/current/{ja,en}_{1..5}_*.png`
- 歯車: `nozworks-brand/png/nozworks_gear_128.png`

## 公開手順 (GitHub Pages、無料)

1. GitHub で**公開**リポジトリ `kn1111/itadaki-burger` を作る
2. このフォルダを push する
   ```
   git init -b main
   git add .
   git commit -m "公式サイト初版"
   git remote add origin https://github.com/kn1111/itadaki-burger.git
   git push -u origin main
   ```
3. リポジトリの Settings → Pages → Source を `main` / `/ (root)` にする
4. 数分後に https://kn1111.github.io/itadaki-burger/ で見られる
5. Steamworks → ストアページ編集 → 基本情報 →「ゲーム ウェブサイト」に URL を入れ、**「変更を公開」まで押す**
6. Google Search Console に URL プレフィックスでサイトを登録し、`sitemap.xml` を送信する

リポジトリ名や独自ドメインを変えるときは、`https://kn1111.github.io/itadaki-burger/` を全ファイルで置換する
(canonical / hreflang / OGP / JSON-LD / robots.txt / sitemap.xml)。

## 文言を足したとき

見出しフォントは使う文字だけに絞ってあるので、**新しい文字を足したらサブセットを作り直す**
(作り直さないと、その字だけ別フォントで出る)。手順は初版作成時のスクリプトと同じで、
両 HTML のテキスト + ASCII を `fontTools.subset` に渡して woff2 / woff を書き出す。

## 後で入れるもの (HTML にコメントで枠がある)

- 予告編: YouTube に上げたら `#about` の iframe を有効にする
- 体験版: Next フェス (2026年10月) で公開されたら `#demo` を有効にする
