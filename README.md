# 平面走査法を実装してみる

## 2-3 木の実装

線分の交点を管理するための探索木として 2-3 木を用いた

[ブログ記事](https://blog.mori-soft.com/entry/2023/07/13/214703) を参照

## 2-3 木を利用した平面走査法

[ブログ記事](https://blog.mori-soft.com/entry/2024/09/14/150118) を参照

### テストケースについて

テストファイルをみればいいのだが、わかりにくいので、下記の Gist (Colaboratory のファイル)を参照

https://gist.github.com/junichim/9ac6e971866e1908495cd2a3736ecbdd
https://gist.github.com/junichim/77b426f9373e2963d34be25fe55ebbc6

## 作業環境

pyenv + venv で管理

システムにインストールした python とは別バージョンの python を利用できるようにするため pyenv を利用
pip3 でインストールするパッケージを関するために venv を利用

pyenv でのバージョン指定

$ pyenv local 3.11.4


.venv という仮想環境を作成
$ python3 -m venv .venv

仮想環境の有効化
$ . .venv/bin/activate

graphviz パッケージのインストール
venv により仮想環境を有効にしているので、そちらにインストールされる
$ pip3 install graphviz

一連の作業環境の構築については、[こちらの記事](https://blog.mori-soft.com/entry/2023/06/09/224950) を参照

