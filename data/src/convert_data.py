import json
import multiprocessing as mp
import os
import subprocess

from typing import Dict, List

import boto3


os.makedirs("./clips/", exist_ok=True)
N = mp.cpu_count()

prefix_dir = "./cv-corpus-24.0-2025-12-05/ru/clips/"

S3_BUCKET_NAME = os.getenv("S3_BUCKET")
S3_ACCESS_KEY = os.getenv("ACCESS_KEY")
S3_SECRET_KEY = os.getenv("SECRET_KEY")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    endpoint_url="https://storage.yandexcloud.net/"
)


def read_manifest(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, "r", encoding="utf-8") as file:
        result = list(map(json.loads, file.readlines()))
    return result


def process_file_and_load_to_s3(dct: Dict[str, str]) -> str:
    audio_filepath = dct["audio_filepath"]
    wav_file = audio_filepath.split("/")[-1]
    mp3_file = wav_file.replace("wav", "mp3")
    mp3_path = f"{prefix_dir}/{mp3_file}"
    # wav_path = f"./{audio_filepath}"

    command = [
        "ffmpeg", "-i", mp3_path,
        "-ar", "16000", "-ac", "1",
        "-f", "wav", "pipe:1",
        "-loglevel", "error"
    ]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        s3_client.upload_fileobj(process.stdout, S3_BUCKET_NAME, audio_filepath)
        process.wait()
        # subprocess.run(command, check=True)
        return f"Uploaded: {audio_filepath}"
    except subprocess.CalledProcessError:
        return f"Error: {os.path.basename(mp3_path)}"


if __name__ == "__main__":
    # files = glob.glob("./cv-corpus-24.0-2025-12-05/ru/clips/*.mp3")
    manifest_dev = read_manifest("manifests/manifest_dev.json")
    manifest_test = read_manifest("manifests/manifest_test.json")
    manifest_train = read_manifest("manifests/manifest_train.json")

    manifest = manifest_dev + manifest_test + manifest_train

    with mp.Pool(processes = N - 1) as pool:
        _ = [
            elem
            for elem in pool.imap_unordered(
                process_file_and_load_to_s3,
                manifest
            )
        ]
