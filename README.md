# ItemDetector
OpenCVを用いて画像の中に定義した画像が存在するかどうかを調べます

## 言語
Python (Ver.2.7)

## 動作に必要なライブラリ
OpenCV

## 例
```python
# 検出用の画像
itemImages = {u"ほげ": "images/hogehoge.png", u"ふげ": "images/hugehuge.png", u"しゃうしゃう": "images/shoushou.png"}
detector = ItemDetector(itemImages)
	
# 調べたい画像データを読み込む
queryImage = detector.loadImage("images/queryImage.png")
print detector.match(queryImage)
```