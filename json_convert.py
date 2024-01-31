import json

def convert_json_structure(input_json):
    output_json = {"images": {}}

    for img_name, img_data in input_json["images"].items():
        output_json["images"][img_name] = {"paragraphs": {}, "words": {}}

        for word_index, word_info in img_data["words"].items():
            output_json["images"][img_name]["words"][word_index.zfill(4)] = {
                "transcription": None,  # You can fill this with actual transcription if available
                "points": word_info["points"],
                "orientation": "Horizontal",  # You can fill this with actual orientation if available
                "language": None,  # You can fill this with actual language information if available
                "tags": [],  # You can fill this with actual tags if available
                "confidence": None,  # You can fill this with actual confidence value if available
                "illegibility": False  # You can fill this with actual illegibility information if available
            }

    return output_json

with open('/data/ephemeral/home/predictions/output_01311211.json', 'r') as file:
    input_data = json.load(file)

output_data = convert_json_structure(input_data)

with open('transoutput.json', 'w') as file:
    json.dump(output_data, file, indent=2)