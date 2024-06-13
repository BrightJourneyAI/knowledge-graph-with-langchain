"""
Script to extract YouTube transcript from multiple video, analyse the contents
and build a knowledge graph on Neo4j. 
"""
import os
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi as yt

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "buildkg123!"
os.environ["OPENAI_API_KEY"] = "sk-"

def extract_transcript(video_ids):
    """
    Extracts transcript text from the supplied video IDs

    Args:
        video_ids (List[str]): 

    Returns:
        str: Transcript of all YouTube videos
    """
    t = yt.get_transcripts(video_ids)
    text = extract_text_elements(t)
    return text

def extract_text_elements(transcript):
    """
    Helper method to extract the text portion of the result fetching
    YouTube transcripts

    Args:
        transcript (tuple): The combined transcripts of all YouTube videos in original format

    Returns:
        str: The extracted text elements of all YouTube transcripts
    """
    transcript_json, _ = transcript 
    text_elements = []
    for key, segments in transcript_json.items():
        for segment in segments:
            text_elements.append(segment['text'])
    return ' '.join(text_elements)

def convert_text_to_graph(unstructured_text, llm, graph):
    """
    Uses the configured LLM to analyse the unstructured text and convert it into a graph

    Args:
        unstructured_text (str): The unstructured text to convert into a graph
        llm (BaseChatModel): The initialized LLM to use
        graph (GraphStore): The initialized graph
    """

    # Create a template to help guide the LLM towards the type of graph we want to build
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system", 
                "You are a running watch expert. Your task today is to identify the " + 
                "various watches in the provided text and compare their features. " +
                "When more than one feature is available on a watch ensure you make that connection"
            )
        ]
    )

    # Init the graph transformer, specifying the nodes, relationships and prompt to guide it
    graph_transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=["Product", "Feature"],
        allowed_relationships=["HAS_FEATURE", "UPGRADE_FROM"],
        prompt=template
    )

    # Convert the unstructured text into a graph
    documents = [Document(page_content=unstructured_text)]
    graph_docs = graph_transformer.convert_to_graph_documents(documents)

    # Write to the Neo4j graph
    graph.add_graph_documents(graph_docs)

def build_kg():
    """
    Construct the graph from unstructured YouTube video transcripts
    """
    # Init our clients
    graph = Neo4jGraph()
    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    # Fetch transcripts for the different YouTube videos
    video_ids = [
            "wYJfVczBORQ", 
            "H-lDmNcKZtI", 
            "YGXNYjL1t00",
            "sY0iHU71k-4",
            "BZ1k_bvupVc"
            ]
    text = extract_transcript(video_ids)

    # Convert the text into graph documents using GPT-4o
    convert_text_to_graph(text, llm, graph)

if __name__ == "__main__":
    build_kg()
