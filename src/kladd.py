
import re

text = "!\[(.*?)\]\((https:\/\/.*?)\)"

matches = re.findall(r"!\[(.*?)\]\((https:\/\/.*?)\)", text)

print(matches)