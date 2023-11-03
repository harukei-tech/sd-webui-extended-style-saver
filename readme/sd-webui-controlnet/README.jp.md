# ControlNetを使用する場合

## 使い方

![controlNet](./../static/images/control_net/image.png)

### 保存時

Preprocessor Previewを予め作ってください。
Saveを実行したとき、Preprocessor Previewの画像を一緒に保存します。
Preprocessor Previewがない場合、imageにある画像を代わりに保存します。

### 適用時

ControlNetの保存データがある場合、
自動で画像欄に画像を入れ、enableにチェックを入れます。

ControlNetを使用している・していないに関わらず
ControlNetのアコーディオンは開きます。
これは、Stable Diffusionのプログラム実行タイミングの制約によるものです。
