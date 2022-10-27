import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
import speech_recognition as sr

import wave
import time
from datetime import datetime




FORMAT        = pyaudio.paInt16
TIME          = 10           # 計測時間[s]
SAMPLE_RATE   = 44100        # サンプリングレート
FRAME_SIZE    = 1024         # フレームサイズ
CHANNELS      = 1            # モノラルかバイラルか
INPUT_DEVICE_INDEX = 0       # マイクのチャンネル
NUM_OF_LOOP   = int(SAMPLE_RATE / FRAME_SIZE * TIME)
CALL_BACK_FREQUENCY = 3      # コールバック呼び出しの周期[sec]


OUTPUT_WAV_FILE = "./output.wav"
OUTPUT_TXT_FILE = "./" + datetime.now().strftime('%Y%m%d_%H_%M') +".txt" # テキストファイルのファイル名を日付のtxtファイルにする



# -------------録音機器のインデックスを探す-------------------
"""
pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    print(pa.get_device_info_by_index(i))
    print()
pa.terminate()
"""



# -----------録音 ------------------------
def record_and_save():
    pa = pyaudio.PyAudio()

    stream = pa.open(format   = FORMAT,
                     channels = CHANNELS,
                     rate     = SAMPLE_RATE,
                     input    = True,
                     input_device_index = INPUT_DEVICE_INDEX,
                     frames_per_buffer  = FRAME_SIZE)

    print("RECORDING...")

    list_frame = []


    for i in range(NUM_OF_LOOP):
        data = stream.read(FRAME_SIZE)
        list_frame.append(data)

    print("RECORDING DONE!")

    # close and terminate stream object "stream"
    stream.stop_stream()
    stream.close()
    pa.terminate()


    wf = wave.open(OUTPUT_PATH, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(list_frame))
    wf.close()


# -----------再生 ------------------------
def play_wav_file():


    wf = wave.open(OUTPUT_PATH, 'rb')
    pa = pyaudio.PyAudio()


    stream = pa.open(format   = pa.get_format_from_width(wf.getsampwidth()),
                     channels = wf.getnchannels(),
                     rate     = wf.getframerate(),
                     output   = True)


    # ファイルの読み込み
    print("Read a file")
    data = wf.readframes(FRAME_SIZE)

    # 各バッファで再生はFRAME SIZE分だけ行われる
    print("play the flie")
    is_to_go = True
    while is_to_go:
        stream.write(data)
        print(len(data), is_to_go)
        data = wf.readframes(FRAME_SIZE)
        is_to_go = len(data) != 0

    stream.close()
    pa.terminate()

    print("DONE")



def callback(in_data, frame_count, time_info, status):
    global sprec 
    try:
        audiodata  = sr.AudioData(in_data, SAMPLE_RATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='ja-JP')
        
        with open(OUTPUT_TXT_FILE,'a') as f: #ファイルの末尾に追記していく
            f.write("\n" + sprec_text)
    
    except sr.UnknownValueError:
        pass
    
    except sr.RequestError as e:
        pass
    
    finally:
        return (None, pyaudio.paContinue)



def main():
    
    with open(OUTPUT_TXT_FILE, 'w') as f: #txtファイルの新規作成
        DATE = datetime.now().strftime('%Y%m%d_%H:%M:%S')
        f.write("日時 : " + DATE + "\n") #最初の一行目に日時を記載する
    

    global sprec 
    
    sprec = sr.Recognizer() # speech recogniserインスタンスを生成
    
    # Audio インスタンス取得
    audio  = pyaudio.PyAudio() 
    
    # ストリームオブジェクトを作成
    stream = audio.open(format             = FORMAT,
                        rate               = SAMPLE_RATE,
                        channels           = CHANNELS,
                        input_device_index = INPUT_DEVICE_INDEX,
                        input              = True, 
                        frames_per_buffer  = SAMPLE_RATE*CALL_BACK_FREQUENCY, # CALL_BACK_FREQUENCY 秒周期でコールバック
                        stream_callback    = callback)
    
    stream.start_stream()
    
    while stream.is_active():
        time.sleep(0.1)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()







if __name__ == '__main__':
    main()