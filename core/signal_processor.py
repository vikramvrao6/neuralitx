import numpy as np
import scipy.signal as signal
import mne

def load_eeg_file(file_path):
    """Load an EEG file using MNE"""
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    return raw

def filter_signal(raw, low_freq=1.0, high_freq=40.0):
    """Apply bandpass filter to remove noise"""
    raw.filter(low_freq, high_freq, verbose=False)
    return raw

def extract_frequency_bands(raw):
    """Extract power in each frequency band"""
    data, times = raw[:]
    sfreq = raw.info['sfreq']
    
    bands = {
        'delta': (0.5, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, 40)
    }
    
    band_powers = {}
    for band_name, (low, high) in bands.items():
        b, a = signal.butter(4, [low / (sfreq/2), high / (sfreq/2)], btype='band')
        filtered = signal.filtfilt(b, a, data[0])
        power = np.mean(filtered ** 2)
        band_powers[band_name] = float(power)
    
    return band_powers

def detect_artifacts(raw):
    """Basic artifact detection using amplitude thresholding"""
    data, times = raw[:]
    threshold = np.mean(np.abs(data)) + 3 * np.std(np.abs(data))
    artifact_mask = np.abs(data[0]) > threshold
    artifact_percentage = (np.sum(artifact_mask) / len(artifact_mask)) * 100
    
    return {
        'artifact_percentage': float(artifact_percentage),
        'is_clean': bool(artifact_percentage < 10.0),
        'threshold_used': float(threshold)
    }

def process_eeg(file_path):
    """Full processing pipeline"""
    raw = load_eeg_file(file_path)
    raw = filter_signal(raw)
    band_powers = extract_frequency_bands(raw)
    artifact_info = detect_artifacts(raw)
    
    return {
        'band_powers': band_powers,
        'artifact_info': artifact_info,
        'duration_seconds': float(raw.times[-1]),
        'n_channels': len(raw.ch_names),
        'sampling_rate': float(raw.info['sfreq'])
    }