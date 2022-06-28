import pandas as pd
import re


def get_data_from_xlsx():
    excel_data = pd.read_excel("file.xlsx", header=None)
    return pd.DataFrame(excel_data)


def delete_header_row(df):
    df_without_header_row = df.drop(df.index[0])
    return df_without_header_row


def get_sentences(df, index):
    original_dialogs = df[index].tolist()
    original_dialogs = list(map(lambda d: str(d), original_dialogs))
    original_dialogs = set(original_dialogs)
    original_dialogs = list(original_dialogs)

    sentences = []

    for text in original_dialogs:
        client_dialogs = re.findall(r'CLIENT:(.+?)BOT:', text + "BOT:", re.DOTALL)

        if len(client_dialogs) == 0:
            sentences.append(text)
        else:
            client_dialogs = get_client_dialogs(client_dialogs)

            for dialog in client_dialogs:
                client_sentences = dialog.split(".")
                sentences = sentences + client_sentences

    sentences = list(map(lambda d: d.strip(), sentences))
    sentences = list(filter(lambda d: d != '', sentences))

    return sentences


def get_client_dialogs(dialogs):
    delimiter_chars = ['?', '!', '.', '\n', 'CLIENT:']

    client_dialogs = []

    for dialog in dialogs:
        filtered_dialog = dialog

        for char in delimiter_chars:
            filtered_dialog = filtered_dialog.replace(char, ".")

        filtered_dialog = filtered_dialog.strip()
        filtered_dialog = re.sub(r"[:,'\";<>\\/`~#%^&*()+]", "", filtered_dialog)
        client_dialogs.append(filtered_dialog.lower())

    return client_dialogs


def get_words_from_sentence(sentence):
    words = list(map(lambda word: word.strip('‌ '), sentence.split(' ')))
    return list(filter(lambda word: word != '', words))


def get_phrase_count_dict(sentences, phrase_word_count):
    phrase_count = {}

    for sentence in sentences:
        words = get_words_from_sentence(sentence)

        for i in range(len(words)):
            if i + phrase_word_count > len(words):
                break

            phrase = " ".join(words[i:i + phrase_word_count])

            if phrase in phrase_count.keys():
                phrase_count[phrase] = phrase_count[phrase] + 1
            else:
                phrase_count[phrase] = 1

    return phrase_count


def sort_phrases(phrase_counts, sort_type="max"):
    reverse = True

    if sort_type == "min":
        reverse = False

    return sorted(phrase_counts.items(), key=lambda p: p[1], reverse=reverse)
