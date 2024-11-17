from flask import Flask, request, jsonify
import hashlib
import zlib

app = Flask(__name__)

def hashSHA(data):
    sha256_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return f"{sha256_hash}"

def hashCRC(data):
    crc_hash = zlib.crc32(data.encode('utf-8'))
    return f"{crc_hash:#010x}"

def binary(data):
    binary_data = ' '.join(format(ord(char), '08b') for char in data)
    return f"{binary_data}"

def deflate(data):
    compressed_data = zlib.compress(data.encode('utf-8'))
    return f"{compressed_data.hex()}"

def RLE(data):
    encoding = []
    prev_char = ''
    count = 1

    for char in data:
        if char != prev_char:
            if prev_char:
                encoding.append(f"{count}{prev_char}")
            count = 1
            prev_char = char
        else:
            count += 1
    if prev_char:
        encoding.append(f"{count}{prev_char}")

    return f"{''.join(encoding)}"

def unsupported_option(option):
    return f"Unsupported option: {option}"

@app.route('/process', methods=['POST'])
def process_request():
    try:
        req_data = request.json
        option = req_data.get('OPTION', '').upper()
        data = req_data.get('DATA', '')

        match option:
            case "SECURE_HASH":
                result = hashSHA(data)
            case "CRC_HASH":
                result = hashCRC(data)
            case "BIN":
                result = binary(data)
            case "DEFLATE":
                result = deflate(data)
            case "RLE":
                result = RLE(data)
            case _:
                result = unsupported_option(option)
        
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
