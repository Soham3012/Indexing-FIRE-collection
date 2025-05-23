from collections import defaultdict
import re
import sys
from pyserini.search.lucene import LuceneSearcher
def parse_fire_topics(filepath):
    queries = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        topics = content.split("<top ")
        for topic in topics[1:]:  # Skip the first split part before first <top>
            num_match = re.search(r"<num>\s*(\d+)", topic)
            title_match = re.search(r"<title>\s*(.+?)\s*</title>", topic)
            if num_match and title_match:
                qid = num_match.group(1).strip()
                title = title_match.group(1).strip()
                queries[qid] = title
    return queries
def extract_tf_and_dl(hits):
    tf_stats = {}
    doc_lens = {}

    for docid in hits:
        doc = hits.doc(docid)
        raw = doc.raw().lower().split()
        tf_dict = defaultdict(int)
        for term in raw:
            tf_dict[term] += 1

        tf_stats[docid] = dict(tf_dict)
        doc_lens[docid] = len(raw)

    return tf_stats, doc_lens
def main():
    ROLLNO=32
    if len(sys.argv) != 3:
        print("Usage: python3 mtc24XX-searcher.py /path/to/index /path/to/topic-file")
        sys.exit(1)

    index_dir = sys.argv[1]
    topic_file = sys.argv[2]
    output_file = "test_.txt"

    searcher = LuceneSearcher(index_dir)
    searcher.set_bm25()  # You can also tune with: set_bm25(k1(controls tf impact)=0.9, b(controls doc length impact)=0.4)

    queries = parse_fire_topics(topic_file)
    with open(output_file, 'w', encoding='utf-8') as fout:
        for qid, query in queries.items():
            hits = searcher.search(query, k=2000)
            print(extract_tf_and_dl(hits))
            for rank, hit in enumerate(hits):
                fout.write(f"{qid}\tQ0\t{hit.docid}\t{rank+1}\t{hit.score:.4f}\t{ROLLNO}\n")

if __name__ == "__main__":
    main()