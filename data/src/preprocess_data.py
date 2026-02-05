from typing import Dict, List

import json
import os
import re

from sklearn.model_selection import train_test_split

import pandas as pd


prefix_dir = "./cv-corpus-24.0-2025-12-05/ru"
PATTERN = re.compile("\w+")

df_durations = pd.read_csv(os.path.join(prefix_dir, "clip_durations.tsv"), sep="\t")
df_durations.rename({"clip": "path"}, axis=1, inplace=True)


def merge_with_durations(dataframe: pd.DataFrame) -> pd.DataFrame:
    """docstring
    """
    new_df = pd.merge(dataframe, df_durations, on="path")

    assert len(dataframe) == len(new_df)
    assert len(dataframe.columns) + 1 == len(new_df.columns)
    assert "duration[ms]" in new_df.columns

    return new_df


def truncate_dataframe(dataframe: pd.DataFrame, hours: float) -> pd.DataFrame:
    """docstring
    """
    hours_total = 0.0
    for i, row in dataframe.iterrows():
        hours_total += (row['duration[ms]'] / 1000 ) / 3600
        if hours_total >= hours:
            return dataframe.iloc[:i]
    return dataframe


def create_manifest(dataframe: pd.DataFrame) -> List[Dict[str, str]]:
    """docstring
    """
    manifest = []
    for _, row in dataframe.iterrows():
        audio_path = row.path.replace("mp3", "wav")
        tmp_dict = {
            "audio_filepath": f"clips/{audio_path}",
            "text": " ".join(re.findall(PATTERN, row.sentence)).lower()
        }
        manifest.append(tmp_dict)

    return manifest


def save_manifest(manifest: List[Dict[str, str]], filename: str) -> None:
    """docstring
    """
    with open(filename, "a", encoding="utf-8") as file:
        for dct in manifest:
            json_str = json.dumps(dct, ensure_ascii=False) + "\n"
            file.write(json_str)


if __name__ == "__main__":
    print("Started data preprocessing")

    df_val = pd.read_csv(os.path.join(prefix_dir, "validated.tsv"), sep="\t")
    df_inval = pd.read_csv(os.path.join(prefix_dir, "invalidated.tsv"), sep="\t")
    df_other = pd.read_csv(os.path.join(prefix_dir, "other.tsv"), sep="\t")

    df_report = pd.read_csv(os.path.join(prefix_dir, "reported.tsv"), sep="\t")
    df_unval_sen = pd.read_csv(os.path.join(prefix_dir, "unvalidated_sentences.tsv"), sep="\t")
    df_val_sen = pd.read_csv(os.path.join(prefix_dir, "validated_sentences.tsv"), sep="\t")

    df_train = pd.read_csv(os.path.join(prefix_dir, "train.tsv"), sep="\t")
    df_test = pd.read_csv(os.path.join(prefix_dir, "test.tsv"), sep="\t")
    df_dev = pd.read_csv(os.path.join(prefix_dir, "dev.tsv"), sep="\t")

    # эту часть не будем брать
    df_inval_durations = merge_with_durations(df_inval)

    # отсюда дополним наборы train, test, dev
    df_val_durations = merge_with_durations(df_val)

    # отсюда возьмём строчки, у которых up_votes > down_votes
    df_other_durations = merge_with_durations(df_other)

    # train
    df_train_durations = merge_with_durations(df_train)

    # test
    df_test_durations = merge_with_durations(df_test)

    # val
    df_dev_durations = merge_with_durations(df_dev)

    # подготовим other
    df_other_filtered = df_other_durations[
        (df_other_durations["up_votes"] >= df_other_durations["down_votes"]) &
        (df_other_durations["sentence"].str.len()) > 0
    ]

    # почистим от слипшихся строк
    df_train_cleaned = df_train[(
            [
                len(elem.split("\n")) == 1
                for elem in df_train["sentence"]
            ]
    )]

    df_test_cleaned = df_test[(
            [
                len(elem.split("\n")) == 1
                for elem in df_test["sentence"]
            ]
    )]

    df_dev_cleaned = df_dev[(
            [
                len(elem.split("\n")) == 1
                for elem in df_dev["sentence"]
            ]
    )]

    df_other_cleaned = df_other_filtered[(
            [
                len(elem.split("\n")) == 1
                for elem in df_other_filtered["sentence"]
            ]
    )]

    df_val_cleaned = df_val_durations[(
            [
                len(elem.split("\n")) == 1
                for elem in df_val_durations["sentence"]
            ]
    )]

    df_inval_cleaned = df_inval_durations[(
            [
                len(elem.split("\n")) == 1
                for elem in df_inval_durations["sentence"]
            ]
    )]

    # объединим всё в один датафрейм
    train_test = pd.concat([df_train_cleaned, df_test_cleaned], ignore_index=True).drop_duplicates(subset="path", keep="first")
    train_test_dev = pd.concat([train_test, df_dev_cleaned], ignore_index=True).drop_duplicates(subset="path", keep="first")
    train_test_dev_val = pd.concat([train_test_dev, df_val_cleaned], ignore_index=True).drop_duplicates(subset="path", keep="first")
    df_full = pd.concat([train_test_dev_val, df_other_cleaned], ignore_index=True).drop_duplicates(subset="path", keep="first")

    # почистим от df_inval
    final_df = df_full[~df_full["path"].isin(df_inval["path"])]

    final_df.drop(["duration[ms]"], axis=1, inplace=True)
    final_df_durations = merge_with_durations(final_df)
    final_df = truncate_dataframe(final_df_durations, hours=90.0)

    X_train, X_val = train_test_split(final_df, test_size=0.33, random_state=42, shuffle=True)
    X_dev, X_test = train_test_split(X_val, test_size=0.5, random_state=42, shuffle=True)

    train_manifest = create_manifest(X_train)
    dev_manifest = create_manifest(X_dev)
    test_manifest = create_manifest(X_test)

    for manifest, name in zip(
        [train_manifest, dev_manifest, test_manifest],
        ["manifests/manifest_train.json", "manifests/manifest_dev.json", "manifests/manifest_test.json"]
        ):
        save_manifest(manifest, name)

    print("Finished data preprocessing")
