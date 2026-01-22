# Сервис по распознаванию речи

**Проектная работа по курсу MLOps**

> Proof of Concept

## Описание проекта

some text

## Структура проекта

```
project-repo/
├── README.md
├── app.py              # основной код приложения
├── models/             # директория для ASR моделей
├── pyproject.toml      # зависимости проекта
├── requirements.txt    # конфигурация проекта
├── static/
│   ├── index.html      # код приложения
│   └── voice.js        # код приложения
├── utils/
│   ├── __init__.py
│   └── wav_tools.py    # код приложения
└── voice/              # директория для сохранения аудио
```

## Требования

- Python 3
- пакетный менеджер [UV](https://docs.astral.sh/uv/)

## Установка

1. Клонируйте репозиторий

```Bash
git clone git@github.com:evgenydarkhanov/otus_mlops_project.git
cd otus_mlops_project
git checkout proof-of-concept
```

2. Установите зависимости

```Bash
uv sync
```

или

```Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Загрузите ASR модель

Модель должна поддерживаться фреймворком [NVIDIA NeMo](https://github.com/NVIDIA-NeMo/NeMo) и быть совместима с классом `nemo.collections.asr.models.EncDecCTCModelBPE`.

В проекте используется [nvidia/stt_ru_conformer_ctc_large](https://huggingface.co/nvidia/stt_ru_conformer_ctc_large)

Примеры подходящих [моделей](https://huggingface.co/nvidia/models?search=stt_conformer_ctc_large).

## Использование

1. 
