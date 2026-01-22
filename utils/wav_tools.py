import os

import numpy as np
import soundfile as sf

from scipy.signal import resample


def get_wavs(dir_path: str) -> list[str]:
    """
    ищет в переданной директории все аудио в формате wav
    """
    wavs = [
        elem for elem in os.listdir(dir_path)
        if elem.endswith("wav")
    ]
    return wavs


def load_and_preprocess_wav(wav_path: str, new_sr: int = 16_000) -> np.ndarray:
    """
    конвертирует стерео в моно
    снижает sample rate до 16_000
    """
    data, sr = sf.read(wav_path)

    # конвертация в моно, если аудио стерео
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # ресемплинг
    if sr != new_sr:
        num_samples = int(len(data) * new_sr / sr)
        data = resample(data, num_samples)

    return data
