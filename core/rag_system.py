BAND_CONTEXT = {
    'delta': "Delta band dominance suggests deep sleep states or possible pathological slowing. In awake subjects, elevated delta may indicate brain injury or encephalopathy.",
    'theta': "Theta band dominance is associated with drowsiness, memory consolidation, and meditative states. Frontal theta is linked to cognitive load and working memory tasks.",
    'alpha': "Alpha band dominance indicates relaxed wakefulness, typically with eyes closed. Alpha suppression during task performance is a normal finding indicating active processing.",
    'beta': "Beta band dominance suggests active thinking, alertness, or anxiety. High beta can also result from certain medications or hyperarousal states.",
    'gamma': "Gamma band dominance is associated with higher cognitive processing, sensory binding, and conscious awareness. Abnormal gamma may indicate neurological conditions."
}

ARTIFACT_KNOWLEDGE = """
Motion artifacts in EEG appear as high amplitude low frequency distortions.
Muscle artifacts appear as high frequency noise above 30 Hz.
Eye blink artifacts create characteristic waveforms in frontal electrodes.
A clean EEG signal should have artifact percentage below 10 percent.
High artifact percentage above 20 percent indicates poor signal quality requiring re-recording.
"""

GENERAL_KNOWLEDGE = """
LFP recordings reflect local population activity of neurons in a specific brain region.
LFP signals contain information about synaptic inputs and local network dynamics.
Frequency band analysis of LFP can reveal oscillatory patterns related to behavior and cognition.
EEG signals represent the summed electrical activity of millions of neurons detected at the scalp.
"""

def get_rag_context(band_powers, artifact_info):
    """Get relevant neuroscience context based on analysis results"""
    dominant_band = max(band_powers, key=band_powers.get)
    band_context = BAND_CONTEXT.get(dominant_band, "")

    if not artifact_info['is_clean']:
        artifact_context = "The signal contains significant artifacts. Consider re-recording or additional preprocessing before analysis." + ARTIFACT_KNOWLEDGE
    else:
        artifact_context = "The signal shows clean quality with artifact percentage below threshold, indicating good electrode contact and minimal movement during recording."

    return f"{band_context}\n\n{artifact_context}\n\n{GENERAL_KNOWLEDGE}"