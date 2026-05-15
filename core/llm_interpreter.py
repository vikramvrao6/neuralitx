import anthropic
import os

def generate_explanation(band_powers, artifact_info, nn_result, rag_context):
    """Send analysis results to Claude for plain English explanation"""
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are a neuroscience expert analyzing EEG/neural signal data for a researcher.

FREQUENCY BAND POWERS:
- Delta (0.5-4 Hz): {band_powers['delta']:.6f}
- Theta (4-8 Hz): {band_powers['theta']:.6f}
- Alpha (8-13 Hz): {band_powers['alpha']:.6f}
- Beta (13-30 Hz): {band_powers['beta']:.6f}
- Gamma (30-40 Hz): {band_powers['gamma']:.6f}

ARTIFACT DETECTION:
- Signal quality: {'Clean' if artifact_info['is_clean'] else 'Artifacts detected'}
- Artifact percentage: {artifact_info['artifact_percentage']:.2f}%

NEURAL NETWORK CLASSIFICATION:
- Classification: {nn_result['classification']}
- Confidence: {nn_result['confidence']:.2f}

CONTEXT: {rag_context[:500]}

Write 2 plain paragraphs explaining these findings for a neuroscience researcher. No markdown, no headers, no bullet points."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def format_results(band_powers, artifact_info, nn_result, rag_context, explanation):
    """Format all results into a structured response"""
    return {
        'band_powers': band_powers,
        'artifact_info': artifact_info,
        'nn_result': nn_result,
        'explanation': explanation,
        'dominant_band': max(band_powers, key=band_powers.get)
    }