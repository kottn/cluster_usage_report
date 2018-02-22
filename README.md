# cluster_usage_report
計算機クラスターの使用率レポートを作るツール

## 利用想定
* Torque で運用されているクラスターで使う。
* 管理者(root)権限になれる人が使う。
* 親ノードのホスト名は`oyanode`で、ユーザー名は`tarou`。

## 準備
### ログイン
```
$ ssh tarou@oyanode
```
### conda をインストール
* ツール内でpython のライブラリをいくつか呼んでいる。
* それらをまるっと導入する conda をインストールする。

:point_right: [インストール方法](https://github.com/kottn/begin_conda) の「**Step 3**」までやる
* とりわけ`conda install`するものはない。anaconda の基本パッケージだけでよい。

### このリポジトリを`clone`する
```
$ cd; git clone https://github.com/kottn/cluster_usage_report
```

### Torque のログをコピーする
```
$ mkdir -p cluster_usage_report/logfiles
$ su -
# cd /home/tarou/cluster_usage_report/logfiles
# cp /var/spool/torque/server_priv/accounting/* ./
```

