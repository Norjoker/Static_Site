
text = "Start **bold** and `code`."
delimiter = "**"

delimiter_indices = [j for j, x in enumerate(text) if x == delimiter]
print(delimiter_indices)