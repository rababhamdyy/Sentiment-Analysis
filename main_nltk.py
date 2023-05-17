import re
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

def load_emotions(emotions_file_path: str) -> dict:
    emotions_dict = {}
    try:
        with open(emotions_file_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split("\t")
                    if len(parts) == 2:
                        emotion, value = parts
                        emotions_dict[emotion] = int(value)
    except (IOError, OSError) as e:
        raise ValueError(f"Could not read {emotions_file_path}: {e}")
    return emotions_dict


def load_stop_words(stop_words_path: str = None) -> set:
    stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                  "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
                  "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
                  "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
                  "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
                  "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
                  "for", "with", "about", "against", "between", "into", "through", "during", "before",
                  "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
                  "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                  "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
                  "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
                  "don", "should", "now"}
    if stop_words_path:
        with open(stop_words_path) as f:
            stop_words |= {line.strip() for line in f}
    return stop_words


def get_category(emotion):
    positive_emotions = ['happy', 'attached', 'loved', 'entitled', 'free', 'attracted']
    if emotion in positive_emotions:
        return 'positive'
    elif emotion == 'hated':
        return 'negative'
    else:
        return 'neutral'


def summarize_emotions(emotion_list):
    emotions_df = pd.DataFrame(emotion_list, columns=['emotion'])
    emotions_df['category'] = emotions_df['emotion'].isin(['happy', 'attached', 'loved', 'entitled', 'free', 'attracted'])
    summary_df = emotions_df.groupby('category').size().reset_index(name='frequency')
    summary_df['category'] = summary_df['category'].apply(lambda x: 'positive' if x else 'neutral')
    summary_df['percentage'] = summary_df['frequency'] / summary_df['frequency'].sum() * 100
    return summary_df


def process_text(input_file_path: str, emotions_file_path: str, stop_words_path: str = None) -> list:
    emotions_dict = load_emotions(emotions_file_path)
    stop_words = load_stop_words(stop_words_path)

    emotion_list = []
    with open(input_file_path) as f:
        for line in f:
            line = line.strip().lower()
            words = re.findall(r"\w+", line)
            for word in words:
                if word in emotions_dict:
                    emotion_list.append(word)
                elif word in stop_words:
                    continue
                else:
                    emotion_list.append('neutral')

    return emotion_list


if __name__ == "__main__":
    input_path = "./read.txt"
    emotions_path = "./emotions.txt"

    emotion_list = process_text(input_path, emotions_path)

    summary_df = summarize_emotions(emotion_list)
    table = tabulate(summary_df, headers=['Category', 'Frequency', 'Percentage'], tablefmt='pretty', showindex=False)
    print('\nEmotion Summary: ')
    print(table)

    labels = summary_df['category']
    percentages = summary_df['percentage']
    colors=['#ff9999','#66b3ff','#99ff99']

    plt.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Emotion Summary')
    plt.show()