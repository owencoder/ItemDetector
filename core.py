# -*- coding: utf-8 -*-
import cv2
import sys

###
#
# 与えられた画像の中に定義された画像が存在するかどうか調べるクラスです
#
###
class ItemDetector:
	# コンストラクタ
	# 引数:
	#	item_images	... 判定時に表示する名称をキーとし、値を判定に使用する画像パスを格納した連想配列
	def __init__(self, itemImages):
		# 特徴量算出アルゴリズムの決定
		# 精度を求めるならSIFT、ちょっと落として速度を稼ぐならSURF
		self.baseAlgorithm = cv2.SIFT()
		# マッチングと検索パラメータの決定
		# アルゴリズムにはFLANN_INDEX_KDTREE(0)を使用
		self.indexParams = dict(algorithm = 0, trees = 5)
		self.searchParams = dict(checks = 50)
		# Feature Matching
		self.flann = cv2.FlannBasedMatcher(self.indexParams, self.searchParams)
		# 判定用画像の設定
		self.setItemImages(itemImages)
	
	# アイテム(判定用)画像のデータを格納します
	# 引数:
	#	item_images ... 判定時に表示する名称をキーとし、値を判定に使用する画像パスを格納した連想配列
	def setItemImages(self, itemImages):
		self.items = []
		# データから画像に対し前処理を行い格納
		for item_name, item in itemImages.items():
			img = self.loadImage(item)
			# 特徴量算出を行う
			des = self.detectAndCompute(img)[1]
			self.items.append({'descriptors': des, 'name': item_name})
	
	# 画像を読み込んで返します
	# 引数:
	#	filePath ... 読み込む画像のファイルパス
	# 戻り値:
	#	グレースケール化 + preProcessImageで前処理された画像データが返されます
	def loadImage(self, filePath):
		#	画像をグレースケールで読み込み
		img = cv2.imread(filePath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
		return self.preProcessImage(img)
	
	# 画像に対して前処理を行います
	# 引数:
	#	srcImage ... 前処理を行う画像データ
	# 戻り値:
	#	ガウシアンぼかしと正規化処理を施した画像データが返されます
	def preProcessImage(self, srcImage):
		#	ガウシアンぼかしを行い特徴点を掴みやすくする
		srcImage = cv2.GaussianBlur(srcImage,(5, 5),0)
		cv2.normalize(srcImage, srcImage, 0, 255, cv2.NORM_MINMAX)
		return srcImage
	
	# baseAlgorithmのアルゴリズムを元に画像から特徴量算出を行います
	# 引数:
	#	srcImage ... 計算する画像データ
	# 戻り値:
	#	結果が代入された配列が返されます
	def detectAndCompute(self, srcImage):
		return self.baseAlgorithm.detectAndCompute(srcImage, None)

	# クエリ画像からマッチングを行います
	# 引数:
	#	queryImage				... 画像データ
	#	distanceThreshold(0.7)	... 類似点を取るときの閾値
	#	matchThreshold(8)		... 類似点の個数からアイテムかどうか判別する閾値
	# 戻り値:
	#	setItemImagesメソッドで格納したデータから合致する画像の名称を返します
	#	どれにも当てはまらなかった場合、空の文字列が返されます
	def match(self, queryImage, distanceThreshold = 0.7, matchThreshold = 8):
		# クエリ画像の前処理と特徴量算出
		queryImage = self.preProcessImage(queryImage)
		queryKp, queryDes = self.detectAndCompute(queryImage)
		
		matchLen = [];
		for item in self.items:
			#	マッチングを行う
			matches = self.flann.knnMatch(item['descriptors'], queryDes, k=2)
			#	結果から類似している点のみを絞り、その数を格納する
			matchLen.append ( 
				len([m for m, n in matches if m.distance < distanceThreshold * n.distance])
			)
		
		# 配列から最大値を調べ、
		# その値が閾値(matchThreshold)以上であればそのアイテムが存在する
		print matchLen
		idx = matchLen.index(max(matchLen))
		if matchLen[idx] >= matchThreshold: return self.items[idx]['name']
		
		# どれにも引っかからなかった
		return ""

if __name__ == '__main__':

	# 検出用の画像
	itemImages = {u"ほげ": "images/hogehoge.png", u"ふげ": "images/hugehuge.png", u"しゃうしゃう": "images/shoushou.png"}
	detector = ItemDetector(itemImages)
	
	# 調べたい画像データを読み込む
	queryImage = detector.loadImage("images/queryImage.png")
	print detector.match(queryImage)