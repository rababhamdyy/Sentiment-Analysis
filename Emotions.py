# This code performs sentiment analysis on a 
# given text file using a pre-defined set of emotions and generates 
# a bar graph of the emotions' frequencies.

import string
import matplotlib.pyplot as plt

# This line imports the pyplot module from the matplotlib library, 
# which is used to create visualizations such as graphs and charts.

from collections import defaultdict, Counter

# This line imports the defaultdict and Counter classes from the collections module.
# These classes are used to create a dictionary with default values 
# and count the frequency of items in a list.

from prettytable import PrettyTable

# This line imports the PrettyTable class from the prettytable module. 
# This class is used to create a formatted table.

def process_text(input_file_path: str, emotions_file_path: str, stop_words_path: str = None,
                 custom_emotions_path: str = None) -> None:
    
# This line defines a function named process_text that takes four arguments: 
# input_file_path, emotions_file_path, stop_words_path, and custom_emotions_path. 

    """
    Process the input text file and generate a bar graph of emotions.

    Arguments:
    - input_file_path: str - path to the input text file.
    - emotions_file_path: str - path to the emotions file.
    - stop_words_path: str (optional) - path to a file containing custom stop words.
    - custom_emotions_path: str (optional) - path to a file containing custom emotions.

    Returns:
    - None
    """
    # reading text file
    try:
        with open(input_file_path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: {input_file_path} not found.")
        return
    
    # This code block attempts to read the input file located at input_file_path 
    # with the utf-8 encoding. If the file is not found, an error message is printed, 
    # and the function returns.

    # converting to lowercase
    lower_case = text.lower()

    # Removing punctuations
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    # This line removes all punctuation from the text using the translate method 


    # splitting text into words
    tokenized_words = cleaned_text.split()

    # loading stop words
    stop_words = set()
    if stop_words_path:
        try:
            with open(stop_words_path, encoding="utf-8") as f:
                stop_words.update(f.read().split())
        except FileNotFoundError:
            print(f"Error: {stop_words_path} not found.")
            return
    else:
        stop_words.update({"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
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
                           "don", "should", "now"})
    
    # This code block defines a set of stop words, 
    # which are common words that are not relevant to the sentiment analysis. 
    # If stop_words_path is provided, this code reads the file and updates the stop_words set 
    # with the words in the file. If the file is not found, an error message is printed, 
    # and the function returns. If stop_words_path is not provided, the default stop words are used.


    # Removing stop words from the tokenized words list
    final_words = [word for word in tokenized_words if word not in stop_words]

    # loading emotions
    emotions = defaultdict(list)
    try:
        with open(emotions_file_path, 'r', encoding="utf-8") as f:
            for line in f:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                try:
                    word, emotion = clear_line.split(':')
                    emotions[word].append(emotion)
                except ValueError:
                    print(f"Error: Invalid format in emotions file: {emotions_file_path}")
                    return
    except FileNotFoundError:
        print(f"Error: {emotions_file_path} not found.")
        return
    
    # This code block reads the emotions file located at emotions_file_path 
    # and creates a dictionary where each key is a word, and the value is a list of 
    # associated emotions. The file is expected to have the format word:emotion,
    # emotion,.... If the file is not found or the format is invalid, an error message is printed,
    # and the function returns.


    # loading custom emotions
    if custom_emotions_path:
        try:
            with open(custom_emotions_path, 'r', encoding="utf-8") as f:
                for line in f:
                    clear_line = line.replace("\n", '').strip()
                    try:
                        word, emotion = clear_line.split(':')
                        emotions[word].append(emotion)
                    except ValueError:
                        print(f"Error: Invalid format in custom emotions file: {custom_emotions_path}")
                        return
        except FileNotFoundError:
            print(f"Error: {custom_emotions_path} not found.")
            return
        
    # This code block reads the custom emotions file located at custom_emotions_path 
    # and adds any new emotions associated with words already in the emotions dictionary. 
    # The file has the same format as the emotions file. If the file is not found or 
    # the format is invalid, an error message is printed, and the function returns.

    # NLP Emotion Algorithm
    # 1) Check if the word in the final word list is also present in the emotions dictionary
    #  - If yes, add all associated emotions to the emotion_list

    emotion_list = []
    for word in final_words:
        if word in emotions:
            emotion_list.extend(emotions[word])
    
    # This code block creates a list of emotions associated with the words in final_words.

    # count the emotions using Counter
    if emotion_list:
        emotion_count = Counter(emotion_list)

        # sort emotions in descending order of frequency
        sorted_emotions = sorted(emotion_count.items(), key=lambda x: x[1], reverse=True)

        # extract emotions and their frequencies
        emotions, frequencies = zip(*sorted_emotions)

        # plot the emotions on the graph
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#999999']
        ax.bar(emotions, frequencies, color=colors)

        # add a title and labels to the graph
        ax.set_title('Emotions in Text', fontsize=20)
        ax.set_xlabel('Emotions', fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)

        # rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=12)

        # add a legend to identify the emotions
        legend_labels = ["happy", "attached", "loved", "hated", "entitled", "free" , "alone", "attracted"]
        legend_handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(legend_labels))]
        ax.legend(legend_handles, legend_labels, fontsize=12)

        # add a grid to the graph
        ax.grid(False)

        # save the graph as a PNG file and display it
        plt.tight_layout()
        plt.savefig('graph.png')
        plt.show()

        # print the emotion list and their frequencies
        print("\nEmotion list: \n")
        print(emotion_list)

        # print the emotion frequency count
        print("\nEmotion frequency count: \n")
        table = PrettyTable()
        table.field_names = ["Emotion", "Frequency"]
        for emotion, frequency in emotion_count.items():
            table.add_row([emotion, frequency])
        # print the table with different formats
        print(table.get_string(border=True, header=True, padding_width=1, tablefmt='fancy_grid'))

    else:
        print("No emotions detected in the input text.")

input_path = "./read.txt"
emotions_path = "./emotions.txt"
process_text(input_path, emotions_path)


# The code performs sentiment analysis on a given text file by identifying emotions associated 
# with the words in the text. It uses a pre-defined set of emotions from an emotions file, 
# and optionally a custom set of emotions from a custom emotions file. The code first reads 
# the input file, removes punctuation and stop words, and creates a list of words called final_words.
# It then checks the emotions associated with each word in final_words and creates a list of
#  emotions called emotion_list. It uses the Counter class to count the frequency of each
#  emotion in emotion_list, sorts the emotions in descending order of frequency, and generates 
#  a bar graph of the emotions' frequencies using the pyplot module from the matplotlib library.
#  Finally, the code prints the list of emotions and their frequencies in a formatted table 
#  using the PrettyTable class from the prettytable module. 