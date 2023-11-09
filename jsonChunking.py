import json
import os

# Create the output directory if it doesn't exist
output_directory = 'chunked_json'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Directory where the original JSON files are stored
json_directory = 'json_output'

# Iterate through the JSON files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        with open(os.path.join(json_directory, filename), 'r') as file:
            data = json.load(file)
            for item in data:
                header = item['header']
                paragraphs = item['paragraphs']

                consolidated_paragraphs = []
                current_paragraph = ""

                # Combine consecutive sentences into a single paragraph
                for paragraph in paragraphs:
                    if paragraph.endswith('.') or paragraph.endswith('!') or paragraph.endswith('?'):
                        current_paragraph += " " + paragraph
                        consolidated_paragraphs.append(current_paragraph.strip())
                        current_paragraph = ""
                    else:
                        current_paragraph += " " + paragraph

                # Create a separate JSON file for each consolidated paragraph
                for paragraph in consolidated_paragraphs:
                    output_data = {"title": header, "body": paragraph}
                    output_filename = f"{header[:20]}_{paragraph[:20]}.json".replace(" ", "_").replace("/", "_")
                    with open(os.path.join(output_directory, output_filename), 'w') as output_file:
                        json.dump(output_data, output_file, indent=4)
