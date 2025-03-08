import google.generativeai as genai
import csv

# Set Gemini API key. Set your own API key.
GEMINI_API_KEY = "GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def read_csv_in_chunks(csv_file_path, chunk_size):
    """
    Generator function to read a CSV file in specified chunk sizes.

    Args:
        csv_file_path (str): Path to the CSV file.
        chunk_size (int): Chunk size.

    Yields:
        list: List containing values from the 'WORD' column of each chunk.
    """
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:  # Open the file
        reader = csv.DictReader(csvfile)  # Read as dictionary with DictReader
        word_list = []
        for i, row in enumerate(reader):
            word_list.append(row['WORD'])  # Add values from the 'WORD' column to the list
            if (i + 1) % chunk_size == 0:  # Process for each chunk size
                yield word_list
                word_list = []
        if word_list:  # Last chunk
            yield word_list


PROMPT_TEMPLATE = """
Write any prompt here.

### Word List:
{word_list}
"""
output_file = 'output.txt'  # Output file name

# Specify any file.
csv_data = 'csvfile/XXXXX.csv'

with open(output_file, 'a', encoding='utf-8') as f:  # Open the file
    for word_list in read_csv_in_chunks(csv_data, chunk_size=100):
        prompt = PROMPT_TEMPLATE.format(word_list="\n".join(word_list))
        #print(prompt)
        response = model.generate_content(prompt)
        print(response.text)
        f.write(response.text + '\n')  # Write to the file

print(f"Results saved to {output_file}.")