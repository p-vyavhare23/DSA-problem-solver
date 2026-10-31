
import os
import re
import networkx as nx
from pyvis.network import Network


# ---------------------------------
# GRAPH FOLDER
# ---------------------------------

GRAPH_DIR = "graph"
GRAPH_FILE = os.path.join(
    GRAPH_DIR,
    "knowledge_graph.html"
)

os.makedirs(GRAPH_DIR, exist_ok=True)


# ---------------------------------
# DSA CONCEPTS AND KEYWORDS
# ---------------------------------

DSA_CONCEPTS = {

    "Binary Search": [
        "binary search",
        "binary searching"
    ],

    "Linear Search": [
        "linear search",
        "sequential search"
    ],

    "Sorted Array": [
        "sorted array",
        "sorted list",
        "ascending order",
        "descending order"
    ],

    "Divide and Conquer": [
        "divide and conquer",
        "divide-and-conquer"
    ],

    "Stack": [
        "stack",
        "lifo"
    ],

    "Push": [
        "push operation",
        "push"
    ],

    "Pop": [
        "pop operation",
        "pop"
    ],

    "Queue": [
        "queue",
        "fifo"
    ],

    "Enqueue": [
        "enqueue"
    ],

    "Dequeue": [
        "dequeue"
    ],

    "Linked List": [
        "linked list",
        "singly linked list",
        "doubly linked list",
        "circular linked list"
    ],

    "Array": [
        "array",
        "arrays"
    ],

    "Tree": [
        "tree",
        "binary tree"
    ],

    "Binary Search Tree": [
        "binary search tree",
        "bst"
    ],

    "Graph": [
        "graph data structure",
        "graph traversal"
    ],

    "BFS": [
        "breadth first search",
        "breadth-first search",
        "bfs"
    ],

    "DFS": [
        "depth first search",
        "depth-first search",
        "dfs"
    ],

    "Sorting": [
        "sorting",
        "sorting algorithm"
    ],

    "Bubble Sort": [
        "bubble sort"
    ],

    "Selection Sort": [
        "selection sort"
    ],

    "Insertion Sort": [
        "insertion sort"
    ],

    "Merge Sort": [
        "merge sort"
    ],

    "Quick Sort": [
        "quick sort"
    ],

    "Heap Sort": [
        "heap sort"
    ],

    "Recursion": [
        "recursion",
        "recursive"
    ],

    "Hashing": [
        "hashing",
        "hash table",
        "hash map"
    ],

    "Heap": [
        "heap data structure",
        "min heap",
        "max heap"
    ],

    "Greedy Algorithm": [
        "greedy algorithm",
        "greedy method"
    ],

    "Dynamic Programming": [
        "dynamic programming",
        "dp"
    ],

    "Time Complexity": [
        "time complexity",
        "big o notation",
        "o(log n)",
        "o(n)",
        "o(n log n)",
        "o(1)",
        "o(n^2)"
    ],

    "Space Complexity": [
        "space complexity",
        "auxiliary space"
    ]
}


# ---------------------------------
# RELATIONSHIPS BETWEEN CONCEPTS
# ---------------------------------

RELATIONSHIPS = {

    "Binary Search": [
        "Sorted Array",
        "Divide and Conquer",
        "Time Complexity"
    ],

    "Linear Search": [
        "Array",
        "Time Complexity"
    ],

    "Stack": [
        "Push",
        "Pop"
    ],

    "Queue": [
        "Enqueue",
        "Dequeue"
    ],

    "Linked List": [
        "Array"
    ],

    "Binary Search Tree": [
        "Tree",
        "Binary Search",
        "Searching"
    ],

    "BFS": [
        "Graph"
    ],

    "DFS": [
        "Graph",
        "Recursion"
    ],

    "Bubble Sort": [
        "Sorting",
        "Time Complexity"
    ],

    "Selection Sort": [
        "Sorting",
        "Time Complexity"
    ],

    "Insertion Sort": [
        "Sorting",
        "Time Complexity"
    ],

    "Merge Sort": [
        "Sorting",
        "Divide and Conquer",
        "Time Complexity"
    ],

    "Quick Sort": [
        "Sorting",
        "Divide and Conquer",
        "Time Complexity"
    ],

    "Heap Sort": [
        "Sorting",
        "Heap",
        "Time Complexity"
    ],

    "Dynamic Programming": [
        "Recursion",
        "Time Complexity"
    ],

    "Greedy Algorithm": [
        "Sorting",
        "Time Complexity"
    ]
}


# ---------------------------------
# FIND MATCHING CONCEPTS
# ---------------------------------

def find_concepts(text):

    text = text.lower()

    found = []

    for concept, keywords in DSA_CONCEPTS.items():

        for keyword in keywords:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(keyword.lower())
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):

                found.append(concept)
                break

    return found


# ---------------------------------
# GENERATE KNOWLEDGE GRAPH
# ---------------------------------

def generate_graph_from_text(
    pdf_text,
    pdf_name="Uploaded PDF"
):

    graph = nx.Graph()

    text = str(pdf_text)

    # Find concepts in the latest input.
    found_concepts = find_concepts(text)

    # Find the main topic from the question.
    question_match = re.search(
        r"Question:\s*(.*?)(?:\n|$)",
        text,
        re.IGNORECASE
    )

    if question_match:

        question = question_match.group(1)

        question_concepts = find_concepts(question)

    else:

        question_concepts = []

    # Select main topic.
    if question_concepts:

        main_topic = question_concepts[0]

    elif found_concepts:

        main_topic = found_concepts[0]

    else:

        main_topic = "DSA Concepts"

    # Remove duplicate concepts.
    concepts = list(dict.fromkeys(found_concepts))

    # Always include the main topic.
    if main_topic not in concepts:
        concepts.insert(0, main_topic)

    # Add main topic node.
    graph.add_node(
        main_topic,
        color="#FF9F43",
        size=35,
        title="Main Topic"
    )

    # Add related concepts.
    for concept in concepts:

        if concept == main_topic:
            continue

        graph.add_node(
            concept,
            color="#4DA8DA",
            size=25
        )

        graph.add_edge(
            main_topic,
            concept,
            title="Related Concept"
        )

    # Add predefined relationships only when both
    # concepts are relevant to the current input.
    for concept in concepts:

        related_concepts = RELATIONSHIPS.get(
            concept,
            []
        )

        for related in related_concepts:

            if (
                related in concepts
                and related != concept
            ):

                graph.add_edge(
                    concept,
                    related,
                    title="Concept Relationship"
                )

    # Add a fallback node if no known DSA keyword is found.
    if len(graph.nodes) == 1:

        graph.add_node(
            "Related DSA Topic",
            color="#4DA8DA",
            size=25
        )

        graph.add_edge(
            main_topic,
            "Related DSA Topic"
        )

    # ---------------------------------
    # CREATE INTERACTIVE PYVIS GRAPH
    # ---------------------------------

    net = Network(
        height="620px",
        width="100%",
        directed=False,
        bgcolor="#FFFFFF",
        font_color="#222222"
    )

    net.from_nx(graph)

    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "font": {
          "size": 18,
          "face": "Arial"
        },
        "borderWidth": 2
      },
      "edges": {
        "color": {
          "color": "#848484",
          "highlight": "#FF9F43"
        },
        "width": 2,
        "smooth": {
          "type": "continuous"
        }
      },
      "physics": {
        "enabled": true,
        "stabilization": {
          "iterations": 100
        },
        "barnesHut": {
          "gravitationalConstant": -3000,
          "centralGravity": 0.3,
          "springLength": 150,
          "springConstant": 0.04
        }
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "zoomView": true
      }
    }
    """)

    # Save a completely new graph each time.
    net.write_html(
        GRAPH_FILE,
        notebook=False,
        open_browser=False
    )

    return len(graph.nodes)
