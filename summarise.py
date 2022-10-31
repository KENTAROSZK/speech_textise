from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor


OUTPUT_ONE_SENTENCE_FILE = "./one_sentence.txt"

N_output = 3






def main():

	# "。"を区切り文字として一つの文章にしたファイルを読み込む。
	with open(OUTPUT_ONE_SENTENCE_FILE) as f:
		document = f.read()
	

	# 自動要約のオブジェクトを生成
	auto_abstractor = AutoAbstractor()

	# トークナイザーにMeCabを指定
	auto_abstractor.tokenizable_doc = MeCabTokenizer()

	# 文書の区切り文字を指定 <--これを使うために"。"を付与する処理をしていた
	auto_abstractor.delimiter_list = ["。", "\n"]

	# ドキュメントの抽象化、フィルタリングを行うオブジェクトを生成
	abstractable_doc = TopNRankAbstractor()

	# 文書の要約を実行
	result_dict = auto_abstractor.summarize(document, abstractable_doc)

	# 要約後の行数を指定
	list_temp = result_dict["summarize_result"][:N_output]
	list_output = []
	for line in list_temp:
		list_output.append(repr(line.rstrip("\n")))

	print(document)

	for _ in range(3):
		print()
	print(str(N_output) + "行でまとめてみた")
	for text in list_output:
		print(text)




if __name__ == '__main__':
    main()