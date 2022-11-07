import os
import pickle
import pandas as pd
from datetime import datetime

import whisper


# インプットファイルや出力ファイルを定義
WAV_FILE = "./output.wav" # 文字起こし&要約したい音声ファイル
PKL_FILE = "./textise.pkl"
OUTPUT_TXT_FILE          = "./" + datetime.now().strftime('%Y%m%d_%H_%M') +".txt" # テキストファイルのファイル名を日付のtxtファイルにする
OUTPUT_ONE_SENTENCE_FILE = "./one_sentence.txt"
OUTPUT_SUMMARISED_FILE   = "./summarised.txt"



def whisper_to_textise_audio():
    """
    whisper ライブラリを使って、音声データをテキストにする
    その結果をresult変数という形で圧縮保存しておく
    """
    if os.path.exists(PKL_FILE):
        pass
    else:
        # tiny < base < small < medium < largeの順に高精度になるが、重くなる。(メモリ不足になる可能性がある)
        model  = whisper.load_model("base")
        result = model.transcribe(WAV_FILE, fp16=False, language="ja", verbose=True)
        
        with open(PKL_FILE, mode='wb') as f:
            pickle.dump(result, f)


def text_and_save():
    """
    whisperの結果ファイルpklをテキストファイル化して保存する
    今回は、文字起こしした結果の生データとその生データを一つの文字列化したものの2つをtxtファイル形式で保存する

    """

    with open(PKL_FILE, mode='rb') as f:
        result = pickle.load(f)

    # whisperのモデルが区切り文字（"。"や"!"など）を作らない場合があるので
    # 区切り文字を強制的に作成する必要がある。
    # そのためにpandasのDataFrameにいったん格納する。
    df_result     = pd.DataFrame(result["segments"])[["text"]]
    series_result = df_result['text']

    # 重複した文章が大量生成されている場合があるので、重複する要素があったら自動で重複排除させる
    list_result = series_result.values.tolist()
    list_result = list(set(list_result))

    # 区切り文字を追加してリストを一つの文字列strに直す。ここでは"。"を区切り文字とする。
    one_sentence = '。'.join(list_result)
    
    # 文字起こしの生データをtxtファイルとして保存
    df_result.to_csv(OUTPUT_TXT_FILE, header=False, index=False)

    # 一つの文字列化したものをtxtファイルとして保存しておく
    with open(OUTPUT_ONE_SENTENCE_FILE, 'w', encoding='utf-8', errors='ignore') as f: #txtファイルの新規作成
        f.write(one_sentence)


def summarise(N_output = 3):
    """
    一つの文字列化したものを読み込んでそれを要約する。
    """
    from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
    from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
    from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

    # "。"を区切り文字として一つの文章にしたファイルを読み込む。
    with open(OUTPUT_ONE_SENTENCE_FILE, encoding='utf-8', errors='ignore') as f:
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

    # 要約した文章は複数行になっているので、アウトプットする行数だけを保存するように変更する
    list_temp = result_dict["summarize_result"]
    if len(list_temp) > N_output:
        list_temp = list_temp[:N_output]
    
    list_output = []
    for line in list_temp:
        #list_output.append(repr(line.rstrip("\n")))
        list_output.append(line)

    with open(OUTPUT_SUMMARISED_FILE, 'w') as f:
        f.writelines(list_output)


def main():
    whisper_to_textise_audio()
    text_and_save()
    summarise()


if __name__ == '__main__':
    main()

