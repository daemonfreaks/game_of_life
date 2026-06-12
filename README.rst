Game of Life
============

A simple terminal implementation of `Conway's Game of Life`_ written in Python.
The game renders the board with curses and advances the universe one generation
at a time.

.. _`Conway's Game of Life`: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Requirements
------------

* Python 3.10 or later
* A terminal environment that supports curses

Running
-------

.. code-block:: console

   python game_of_life.py

Controls
--------

* ``Up``: Increase the simulation speed
* ``Down``: Decrease the simulation speed
* ``r``: Toggle a random cell
* ``q``: Quit

Development Setup
-----------------

Install the development dependencies from ``pyproject.toml``.

.. code-block:: console

   python -m pip install --upgrade pip
   python -m pip install --group dev

The ``--group`` option requires a recent version of pip, so upgrading pip first
is recommended.

Quality Checks
--------------

.. code-block:: console

   ruff check .
   mypy .
   pytest

Project Files
-------------

* ``game_of_life.py``: Game logic and terminal UI
* ``test_game_of_life.py``: Tests
* ``pyproject.toml``: Project metadata, development dependencies, and tool
  configuration


ライフゲーム
============

Pythonで実装したシンプルな端末版の `ライフゲーム`_ です。cursesを使って盤面を表示し、世代を1ステップずつ進めます。

.. _`ライフゲーム`: https://ja.wikipedia.org/wiki/%E3%83%A9%E3%82%A4%E3%83%95%E3%82%B2%E3%83%BC%E3%83%A0

動作環境
--------

* Python 3.10 以上
* cursesが使える端末環境

実行方法
--------

.. code-block:: console

   python game_of_life.py

操作方法
--------

* ``Up``: シミュレーションを速くする
* ``Down``: シミュレーションを遅くする
* ``r``: ランダムなセルを反転する
* ``q``: 終了する

開発環境
--------

``pyproject.toml`` に定義されている開発用依存関係をインストールします。

.. code-block:: console

   python -m pip install --upgrade pip
   python -m pip install --group dev

``--group`` オプションを使うには新しいバージョンのpipが必要なので、先にpipを更新することを推奨します。

品質チェック
------------

.. code-block:: console

   ruff check .
   mypy .
   pytest

プロジェクト構成
----------------

* ``game_of_life.py``: ゲームロジックと端末UI
* ``test_game_of_life.py``: テスト
* ``pyproject.toml``: プロジェクトメタデータ、開発用依存関係、ツール設定
