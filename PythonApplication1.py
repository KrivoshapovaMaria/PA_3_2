import os
import zipfile

def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def compress_lzw(uncompressed):
    dictionary = {chr(i): i for i in range(256)}
    current_code = 256
    result = []
    string = ""

    for symbol in uncompressed:
        new_string = string + symbol
        if new_string in dictionary:
            string = new_string
        else:
            result.append(dictionary[string])
            dictionary[new_string] = current_code
            current_code += 1
            string = symbol

    if string:
        result.append(dictionary[string])

    return result

def decompress_lzw(compressed):
    dictionary = {i: chr(i) for i in range(256)}
    current_code = 256
    previous_code = compressed[0]
    string = dictionary[previous_code]
    result = string
    uncompressed = [string]
    previous_string = "" 

    for code in compressed[1:]:
        if code in dictionary:
            string = dictionary[code]
        elif code == current_code:
            string = previous_string + previous_string[0]
        else:
            raise ValueError('Некоректний код')

        result += string
        dictionary[current_code] = previous_string + string[0]
        current_code += 1
        previous_string = string

    return result


def compress_file(input_file_path, output_file_path):
    data = read_data(input_file_path)
    compressed_data = compress_lzw(data)
    write_data(output_file_path, bytes(compressed_data))

def decompress_file(input_file_path, output_file_path):
    compressed_data = read_data(input_file_path)
    decompressed_data = decompress_lzw(compressed_data)
    write_data(output_file_path, decompressed_data)

choice = input("Enter 'encode' for encoding or 'decode' for decoding: ")

if choice.lower() == 'encode':
    # Кодування
    input_file_path = 'input.txt'
    compressed_archive_path = 'compressed_output.zip'

    original_data = read_data(input_file_path)
    compressed_data = compress_lzw(original_data)

    with zipfile.ZipFile(compressed_archive_path, 'w') as compressed_archive:
        compressed_archive.writestr('compressed_data.txt', str(compressed_data))

    print("File encoded and compressed successfully.")

elif choice.lower() == 'decode':
    # Декодування
    compressed_archive_path = 'compressed_output.zip'
    decompressed_file_path = 'decompressed_output.txt'

    with zipfile.ZipFile(compressed_archive_path, 'r') as compressed_archive:
        compressed_data = compressed_archive.read('compressed_data.txt')

    decompressed_data = decompress_lzw(eval(compressed_data))
    write_data(decompressed_file_path, decompressed_data)

    print("File decompressed and decoded successfully.")

else:
    print("Invalid choice. Please enter 'encode' or 'decode'.")
