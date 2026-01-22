import logging
import os
import hashlib
import subprocess
import time
from pathlib import Path

from fastapi import (
    Body,
    FastAPI,
    File,
    UploadFile,
    HTTPException
)
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse
)
from fastapi.staticfiles import StaticFiles

import nemo.collections.asr as nemo_asr
import torch

from utils import wav_tools


### BACKEND PART ###
app = FastAPI(title="ASR Service")

# создаем директорию для сохранения аудио
VOICE_DIR = Path("voice")
VOICE_DIR.mkdir(exist_ok=True)

# монтируем директорию для сохранения аудио
app.mount(
    "/voice",
    StaticFiles(directory="voice"),
    name="voice"
)

# монтируем директорию для HTML + JS
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


### ASR PART ###
# пробуем отключить логи NeMo
logging.getLogger("nemo_logger").disabled = True

MODEL_PATH = "./models/stt_ru_conformer_ctc_large.nemo"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

asr_model = nemo_asr.models.EncDecCTCModelBPE.restore_from(
    restore_path=MODEL_PATH,
    map_location=DEVICE
)


def clear_dir(directory: str, filename: str):
    """
    Оставляем только один файл в директории
    """
    for elem in os.listdir(directory):
        if elem != filename:
            os.remove(elem)


@app.post("/api/voice")
async def upload_voice(voice: UploadFile = File(...)):
    """
    Сохраняем аудио
    """
    try:
        # проверяем тип файла
        if not voice.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail="Only audio files are allowed"
            )

        # генерируем уникальное имя файла
        file_extension = voice.content_type.split('/')[-1]
        unique_filename = hashlib.md5(
            f"{time.time()}_{voice.filename}".encode()
        ).hexdigest() + f".{file_extension}"

        # генерируем путь к файлу
        file_path = VOICE_DIR / unique_filename

        # сохраняем файл
        content = await voice.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # URL для доступа к файлу
        file_url = f"/voice/{unique_filename}"

        # конвертируем в WAV, mono, 16kHz
        new_wav = file_url.split('.')[0] + '.wav'
        subprocess.run(
            f"ffmpeg -i .{file_url} -ar 16000 -ac 1 .{new_wav}",
            shell=True,
            capture_output=False,
            check=True
        )

        # удаляем WEBM
        subprocess.run(
            f"rm .{file_url}",
            shell=True,
            capture_output=False,
            check=True
        )

        return {
            "result": "OK",
            "data": new_wav
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "result": "ERROR",
                "data": str(e)
            }
        )


@app.post("/api/transcribe")
async def transcribe_voice(data: dict = Body(...)):
    """
    Транскрибируем аудио
    """
    try:
        filename = data.get("filename")

        wav = wav_tools.load_and_preprocess_wav(f".{filename}")
        with torch.no_grad():
            transcription = asr_model.transcribe(wav)[0].text

        return {
            "result": "OK",
            "data": transcription
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "result": "ERROR",
                "data": str(e)
            }
        )


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Главная страница - возвращаем HTML
    """
    return RedirectResponse("/static/index.html")
