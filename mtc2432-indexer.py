import sys
import subprocess
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 mtc24XX-indexer.py /path/to/json_docs/ /path/to/output_index/")
        sys.exit(1)

    input_dir = sys.argv[1]
    index_dir = sys.argv[2]

    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        sys.exit(1)

    command = [
        "python", "-m", "pyserini.index.lucene",
        "--collection", "TrecCollection",
        "--generator", "DefaultLuceneDocumentGenerator",
        "--input", input_dir,
        "--index", index_dir,
        "--threads", "4",
        "--language", "en",
        "--stemmer", "none",
        "--storeRaw",
        "--storeContents",
        "--storeDocvectors",
        "--storePositions"
    ]

    print("Running indexing with StandardAnalyzer-equivalent settings...")
    subprocess.run(command)

if __name__ == "__main__":
    main()
