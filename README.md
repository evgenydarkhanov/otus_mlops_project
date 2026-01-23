# Сервис по распознаванию речи

**Проектная работа по курсу MLOps**

> Proof of Concept

## Описание проекта

Проект реализует веб-сервис для распознавания речи с использованием моделей машинного обучения. Приложение записывает входящее аудио, сохраняет запись в формате WAV и транскрибирует в текст. Прототип демонстрационный и не является полноценным продуктом.

## Структура проекта

```
project-repo/
├── README.md
├── app.py              # основной код приложения
├── models/             # директория для ASR моделей
├── pyproject.toml      # конфигурация проекта
├── requirements.txt    # зависимости проекта
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
- пакетный менеджер [UV](https://docs.astral.sh/uv/) (опционально)

## Установка

1. Клонируйте репозиторий

```Bash
git clone https://github.com/evgenydarkhanov/otus_mlops_project.git
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

> установка `nemo_toolkit[asr]` может быть длительной.

3. Загрузите ASR [модель](https://huggingface.co/nvidia/stt_ru_conformer_ctc_large).

Файл модели с расширением `.nemo` поместите в директорию `models/`.

## Использование

Запустите приложение

```Bash
uvicorn app:app --reload
```

или

```Bash
uv run uvicorn app:app --reload
```

Далее переходите в браузер по сгенерированной ссылке.
