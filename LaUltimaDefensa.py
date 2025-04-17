read = "a01b01c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a03b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b^5c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|"

def string_to_matrix(input_string):
    if input_string.endswith('|'):
        input_string = input_string[:-1]
    
    rows = input_string.split('|')
    
    matrix = []
    for row in rows:
        cells = [row[i+1] for i in range(0, len(row), 3)]

        matrix.append(cells)
    
    matrix = matrix[::-1]
    
    return matrix

result_matrix = string_to_matrix(read)

for row in result_matrix:
    print(" ".join(row))

x = 0
y = 0
for i in range(len(result_matrix)):
    for j in range(len(result_matrix[i])):
        if result_matrix[i][j] == '^':
            x = j
            y = i

print(y - 1)
print(x)

# missed, started the count in 0 