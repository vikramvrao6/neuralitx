from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FakeEmbeddings

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

BAND_CONTEXT = {
    'delta': "Delta band dominance suggests deep sleep states or possible pathological slowing. In awake subjects, elevated delta may indicate brain injury or encephalopathy.",
    'theta': "Theta band dominance is associated with drowsiness, memory consolidation, and meditative states. Frontal theta is linked to cognitive load and working memory tasks.",
    'alpha': "Alpha band dominance indicates relaxed wakefulness, typically with eyes closed. Alpha suppression during task performance is a normal finding indicating active processing.",
    'beta': "Beta band dominance suggests active thinking, alertness, or anxiety. High beta can also result from certain medications or hyperarousal states.",
    'gamma': "Gamma band dominance is associated with higher cognitive processing, sensory binding, and conscious awareness. Abnormal gamma may indicate neurological conditions."
}

def get_rag_context(band_powers, artifact_info):
    """Get relevant neuroscience context based on analysis results"""
    dominant_band = max(band_powers, key=band_powers.get)
    artifact_status = "high artifact contamination" if not artifact_info['is_clean'] else "clean signal quality"
    
    band_context = BAND_CONTEXT.get(dominant_band, "")
    
    artifact_context = ""
    if not artifact_info['is_clean']:
        artifact_context = "The signal contains significant artifacts. Motion artifacts appear as high amplitude low frequency distortions. Muscle artifacts appear as high frequency noise. Consider re-recording or additional preprocessing."
    else:
        artifact_context = "The signal shows clean quality with artifact percentage below threshold. This indicates good electrode contact and minimal movement during recording."
    
    context = f"{band_context}\n\n{artifact_context}\n\n{NEUROSCIENCE_KNOWLEDGE}"
    return context