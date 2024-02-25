import urllib.parse
import json

# URL-encoded JSON string
encoded_str = '%7B%22action%22:%22autopage%22,%22phone_id%22:681647996,%22phone_position%22:1,%22phone_list_number%22:0,%22phone_state%22:1,%22real_marka_id%22:79,%22real_model_id%22:2104,%22photo_count%22:171,%22race%22:220%7D'

# Decode the URL-encoded string to JSON
decoded_json_str = urllib.parse.unquote(encoded_str)

# Parse the JSON string
data = json.loads(decoded_json_str)

# Extract the phone number
print(data)
