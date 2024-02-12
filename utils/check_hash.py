from utils.config_reader import classification_config
import hashlib


def calculate_sha256_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        # Read the file in chunks to handle large files
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


if __name__ == "__main__":
    print("Model HASH: ", calculate_sha256_hash(classification_config["model_path"]))
