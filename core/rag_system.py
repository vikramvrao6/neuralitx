from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

# Neuroscience knowledge base - we'll expand this with real papers later
NEUROSCIENCE_KNOWLEDGE = """
Delta waves (0.5-4 Hz) are high amplitude brain waves associated with deep sleep and unconscious processes.
Elevated delta activity during wakefulness may indicate brain injury or pathological conditions.

Theta waves (4-8 Hz) are associated with drowsiness, meditation, and memory processing.
Elevated theta in frontal regions is linked to cognitive tasks and working memory.
Abnormal theta activity can indicate neurological disorders.

Alpha waves (8-13 Hz) are prominent during relaxed wakefulness with eyes closed.
Alpha suppression occurs during active mental processing and visual attention.
Reduced alpha power may indicate anxiety or hyperarousal states.

Beta waves (13-30 Hz) are associated with active thinking, focus, and alertness.
High beta activity can indicate anxiety, stress, or certain medications.
Beta activity is typically dominant during active concentration.

Gamma waves (30-40 Hz) are associated with higher cognitive functions and consciousness.
Gamma synchronization is linked to sensory binding and working memory.
Abnormal gamma patterns may be associated with neurological conditions.

Motion artifacts in EEG appear as high amplitude, low frequency distortions.
Muscle artifacts appear as high frequency noise above 30 Hz.
Eye blink artifacts create characteristic waveforms in frontal electrodes.
A clean EEG signal should have artifact percentage below 10 percent.
High artifact percentage above 20 percent indicates poor signal quality requiring re-recording.

LFP recordings reflect local population activity of neurons in a specific brain region.
LFP signals contain information about synaptic inputs and local network dynamics.
Frequency band analysis of LFP can reveal oscillatory patterns related to behavior and cognition.
"""

def build_knowledge_base():
    """Build FAISS vector store from neuroscience knowledge"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    
    chunks = text_splitter.create_documents([NEUROSCIENCE_KNOWLEDGE])
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def query_knowledge_base(vectorstore, query, k=3):
    """Query the knowledge base for relevant context"""
    docs = vectorstore.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in docs])
    return context

def get_rag_context(band_powers, artifact_info):
    """Get relevant neuroscience context for the analysis results"""
    vectorstore = build_knowledge_base()
    
    # Build query from analysis results
    dominant_band = max(band_powers, key=band_powers.get)
    artifact_status = "high artifact" if not artifact_info['is_clean'] else "clean signal"
    
    query = f"dominant {dominant_band} waves {artifact_status} EEG analysis"
    context = query_knowledge_base(vectorstore, query)
    
    return context