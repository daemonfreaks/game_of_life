# Copilot Instructions

## プロジェクト概要

コンウェイのライフゲーム（Conway's Game of Life）のターミナル実装です。
Python の標準ライブラリ `curses` を使って盤面を描画し、世代を 1 ステップずつ進めます。

- **バージョン**: 0.1.0
- **動作環境**: Python 3.10 以上、curses が使えるターミナル環境
- **外部ランタイム依存**: なし（標準ライブラリのみ使用）

## 技術スタック

| カテゴリ | 内容 |
|---|---|
| 言語 | Python 3.10+ |
| ランタイム依存 | なし（stdlib: `curses`, `argparse`, `dataclasses`, `random`, `time`） |
| リント | [ruff](https://docs.astral.sh/ruff/) |
| 型チェック | [mypy](https://mypy.readthedocs.io/)（strict モード） |
| テスト | [pytest](https://docs.pytest.org/) + [pytest-cov](https://pytest-cov.readthedocs.io/) |
| CI/CD | GitHub Actions |

## ディレクトリ構造

```
game_of_life/
├── .github/
│   ├── copilot-instructions.md   # このファイル
│   └── workflows/                # GitHub Actions ワークフロー
├── game_of_life.py               # ゲームロジック・ターミナル UI
├── test_game_of_life.py          # ユニットテスト
├── pyproject.toml                # プロジェクトメタデータ・ツール設定
├── README.rst                    # ドキュメント（日英）
└── LICENSE
```

## コーディング規約

### 型ヒント

- すべての関数・メソッドに型ヒントを付与する（mypy strict に準拠）
- `Any` の使用は原則禁止

### フォーマット・リント

- **ruff** を使用してフォーマットとリントを行う
- 設定値: `line-length = 88`, `target-version = "py310"`
- 有効なルールセット: `E`, `F`, `W`, `I`, `UP`, `B`, `SIM`

```bash
ruff check .
```

### docstring

- **すべての public クラス・メソッド・関数**に docstring を記述する
- 記述言語: **日本語**
- 形式: Sphinx スタイル（`:param:` / `:type:` / `:return:` / `:rtype:`）

```python
def compute_next_state(self, alive_neighbors: int) -> None:
    """
    次の世代の状態を計算する。

    :param alive_neighbors: 周囲の生きているセルの数
    :type alive_neighbors: int
    """
```

### その他

- `dataclass` を活用してデータ保持クラスを実装する
- ミュータブル / イミュータブルを意識して `frozen=True` を適切に使う
- マジックナンバーは定数として切り出す

## テスト方針

- テストファイルの命名: `test_*.py`
- テストは関数単位・クラス単位で分離する
- **ブランチカバレッジ**を計測し、カバレッジの低下するコードを追加しない

```bash
pytest  # カバレッジレポートも同時出力
```

## ブランチ・PR ルール（GitHub Flow）

- `main` ブランチは常にデプロイ可能な状態を保つ
- 作業は `feature/xxx` / `fix/xxx` / `chore/xxx` などのブランチを切って行う
- 作業完了後は `main` へ PR を作成してマージする
- **PR マージ前に以下がすべてパスすること**:
  - `ruff check .`（リント）
  - `mypy .`（型チェック）
  - `pytest`（テスト・カバレッジ）

## コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) に従う。

```
<type>: <概要（日本語 or 英語）>
```

| type | 用途 |
|---|---|
| `feat` | 新機能の追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `refactor` | 動作を変えないコードの整理 |
| `test` | テストの追加・修正 |
| `chore` | ビルド設定・ツール設定の変更 |
| `perf` | パフォーマンス改善 |

**例**:
```
feat: セルの色を設定できるオプションを追加
fix: 境界セルの近傍カウントが誤る問題を修正
test: blinker パターンの振動テストを追加
```

## CI/CD（GitHub Actions）

PR および `main` へのプッシュ時に以下を自動実行する:

1. `ruff check .` — リント
2. `mypy .` — 型チェック
3. `pytest` — テスト・カバレッジ計測

ローカルでも PR 前に必ず上記コマンドを実行してから push すること。

## 開発環境セットアップ

```bash
python -m pip install --upgrade pip
python -m pip install --group dev
```
