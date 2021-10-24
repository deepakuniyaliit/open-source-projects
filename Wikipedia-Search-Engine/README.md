# Wikipedia Search Engine
This is a search engine built on the full English corpus of wikipedia (~80 GB)

## Code Files
`Indexer.py` - File containing all functions related to XML parsing and text preprocessing, the code for indexing.
`Merge.py` - File with functions related to k-way mergesort algorithm and creates secondary index.
`search.py` - Main file containing all the code for Query Processing\

## About Project
First wiki-dump xml file is parsed and inverted_index file is created, by splitting and merging index files. Then query is searched and top 10 results (doc title) are returned using ranking mechanism (tf-idf).

## Prerequisites
- Python3
- nltk
- etree
- stop words list

## Execution of Code
- Run Indexer.py with path to dump and folder to index as command line arguments.
`python Indexer.py <path to wiki-dump> <path to folder where index will be stored> <stats file name>`
- Run Merge.py - Will sort the index and create secondary index
`python Merge.py`
- Run search.py - will take queries from "queries.txt" and output top 10 results for each query and the time taken to search result in "queries_op.txt" file.
`python search.py`

## Types of Queries
**Normal query** - Any sequence of words that doesn’t satisfy the above conditions is considered a normal query eg: “Sachin Tendulkar”

**Field query** - Assuming that fields are small letters(b, i, c, t, r, e) followed by colon and the fields are space separated. eg: “b:sachin i:2003 c:sports”