import torch
import torch.nn as nn
import numpy as np

class ArtifactClassifier(nn.Module):
    """Neural network to classify EEG segments as clean or artifacted"""
    def __init__(self, input_size=5):
        super(ArtifactClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.network(x)

def prepare_features(band_powers):
    """Convert band powers dict to tensor for NN input"""
    features = [
        band_powers['delta'],
        band_powers['theta'],
        band_powers['alpha'],
        band_powers['beta'],
        band_powers['gamma']
    ]
    return torch.tensor(features, dtype=torch.float32)

def normalize_features(features):
    """Normalize features to 0-1 range"""
    min_val = features.min()
    max_val = features.max()
    if max_val - min_val == 0:
        return features
    return (features - min_val) / (max_val - min_val)

def load_model(model_path=None):
    """Load trained model or return untrained model"""
    model = ArtifactClassifier(input_size=5)
    if model_path:
        try:
            model.load_state_dict(torch.load(model_path))
            model.eval()
        except:
            pass
    return model

def run_inference(band_powers, model_path='models/trained_model.pt'):
    """Run artifact classification on band powers"""
    model = load_model(model_path)
    model.eval()
    
    features = prepare_features(band_powers)
    features = normalize_features(features)
    
    with torch.no_grad():
        output = model(features.unsqueeze(0))
        confidence = float(output.item())
        is_artifact = confidence > 0.5
    
    return {
        'is_artifact': bool(is_artifact),
        'confidence': float(confidence),
        'classification': 'artifact' if is_artifact else 'clean'
    }