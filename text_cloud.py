import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import re
from collections import Counter
import matplotlib
matplotlib.use('TkAgg')  # Use the TkAgg backend for matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import unittest


class WordCloudGenerator:
    def __init__(self):
        self.file_path = ''
        self.max_words = 200
        self.background_color = 'white'
        self.word_colors = ['black']
        self.width = 800
        self.height = 400

    def load_text(self):
        with open(self.file_path, 'r') as file:
            return file.read()

    def process_text(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def count_words(self, processed_text):
        return Counter(processed_text)

    def random_color_func(self, *args, **kwargs):
        return random.choice(self.word_colors)

    def generate_word_cloud(self):
        try:
            text = self.load_text()
            processed_text = self.process_text(text)
            word_count = self.count_words(processed_text)

            wordcloud = WordCloud(width=self.width, height=self.height, max_words=self.max_words,
                                  background_color=self.background_color, color_func=self.random_color_func)
            wordcloud.generate_from_frequencies(word_count)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


class WordCloudApp:
    def __init__(self, root):
        self.root = root
        self.generator = WordCloudGenerator()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Word Cloud Generator")

        # Frame for file selection
        self.frame_file = tk.Frame(self.root)
        self.frame_file.pack(pady=10)
        self.label_file = tk.Label(self.frame_file, text="Select a text file:")
        self.label_file.pack(side=tk.LEFT, padx=5)
        self.entry_file = tk.Entry(self.frame_file, width=50)
        self.entry_file.pack(side=tk.LEFT, padx=5)
        self.button_browse = tk.Button(self.frame_file, text="Browse", command=self.browse_file)
        self.button_browse.pack(side=tk.LEFT, padx=5)

        # Frame for options
        self.frame_options = tk.Frame(self.root)
        self.frame_options.pack(pady=10)
        self.label_max_words = tk.Label(self.frame_options, text="Max Words:")
        self.label_max_words.pack(side=tk.LEFT, padx=5)
        self.entry_max_words = tk.Entry(self.frame_options, width=5)
        self.entry_max_words.pack(side=tk.LEFT, padx=5)
        self.entry_max_words.insert(0, str(self.generator.max_words))
        self.label_bg_color = tk.Label(self.frame_options, text="Background Color:")
        self.label_bg_color.pack(side=tk.LEFT, padx=5)
        self.button_bg_color = tk.Button(self.frame_options, text="Select Color", command=self.choose_bg_color)
        self.button_bg_color.pack(side=tk.LEFT, padx=5)

        self.label_text_color = tk.Label(self.frame_options, text="Text Colors:")
        self.label_text_color.pack(side=tk.LEFT, padx=5)
        self.button_text_color = tk.Button(self.frame_options, text="Select Colors", command=self.choose_text_colors)
        self.button_text_color.pack(side=tk.LEFT, padx=5)

        # Frame for color displays
        self.frame_colors = tk.Frame(self.root)
        self.frame_colors.pack(pady=10)
        self.bg_color_display = tk.Label(self.frame_colors, text="Background", width=10, background=self.generator.background_color)
        self.bg_color_display.pack(side=tk.LEFT, padx=5)
        self.text_colors_display = tk.Frame(self.frame_colors, width=100, height=20)
        self.text_colors_display.pack(side=tk.LEFT, padx=5)

        # Frame for generate button
        self.frame_generate = tk.Frame(self.root)
        self.frame_generate.pack(pady=10)
        self.button_generate = tk.Button(self.frame_generate, text="Generate Word Cloud", command=self.generate_word_cloud)
        self.button_generate.pack()

    def browse_file(self):
        self.generator.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.generator.file_path:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, self.generator.file_path)

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.generator.background_color = color
            self.bg_color_display.config(background=color)

    def choose_text_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.generator.word_colors.append(color)
            color_label = tk.Label(self.text_colors_display, text="", background=color, width=2)
            color_label.pack(side=tk.LEFT, padx=2)
            color_label.bind("<Button-1>", lambda e, c=color: self.remove_text_color(e, c))

    def remove_text_color(self, event, color):
        label = event.widget
        label.destroy()
        self.generator.word_colors.remove(color)

    def generate_word_cloud(self):
        try:
            self.generator.max_words = int(self.entry_max_words.get())
        except ValueError:
            messagebox.showerror("Error", "Max Words must be an integer")
            return
        self.generator.generate_word_cloud()


def main():
    root = tk.Tk()
    root.minsize(600, 200)  # Set minimum window size
    root.maxsize(1200, 800)  # Set maximum window size
    app = WordCloudApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Test functions
class TestWordCloudGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = WordCloudGenerator()
        self.sample_text = "Hello world! This is a test. Hello again."

    def test_load_text(self):
        self.generator.file_path = 'sample.txt'
        with open('sample.txt', 'w') as file:
            file.write(self.sample_text)
        self.assertEqual(self.generator.load_text(), self.sample_text)

    def test_process_text(self):
        processed_text = self.generator.process_text(self.sample_text)
        expected = ['hello', 'world', 'this', 'is', 'a', 'test', 'hello', 'again']
        self.assertEqual(processed_text, expected)

    def test_count_words(self):
        processed_text = self.generator.process_text(self.sample_text)
        word_count = self.generator.count_words(processed_text)
        expected = {'hello': 2, 'world': 1, 'this': 1, 'is': 1, 'a': 1, 'test': 1, 'again': 1}
        self.assertEqual(word_count, expected)

    def test_random_color_func(self):
        self.generator.word_colors = ['red', 'blue', 'green']
        color = self.generator.random_color_func()
        self.assertIn(color, self.generator.word_colors)

    def test_generate_word_cloud(self):
        self.generator.file_path = 'sample.txt'
        with open('sample.txt', 'w') as file:
            file.write(self.sample_text)
        try:
            self.generator.generate_word_cloud()
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
