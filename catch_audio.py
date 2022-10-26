import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write

import wave
import time




FORMAT        = pyaudio.paInt16
TIME          = 10            # 計測時間[s]
SAMPLE_RATE   = 44100        # サンプリングレート
FRAME_SIZE    = 1024         # フレームサイズ
CHANNELS      = 1            # モノラルかバイラルか
INPUT_DEVICE_INDEX = 0       # マイクのチャンネル
OUTPUT_PATH   = "./output.wav"
NUM_OF_LOOP   = int(SAMPLE_RATE / FRAME_SIZE * TIME)



# -------------録音機器のインデックスを探す-------------------
"""
for i in range(pa.get_device_count()):
    print(pa.get_device_info_by_index(i))
    print()
"""



# -----------録音 ------------------------


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




time.sleep(TIME+2)



# -----------再生 ------------------------

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