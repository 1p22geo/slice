import numpy as np
import laion_clap
import fnmatch
import os


model = laion_clap.CLAP_Module(enable_fusion=False)
model.load_ckpt(model_id=1)

# Directly get audio embeddings from audio files
audio_file = [
    "./data/SAMPLES/ACTUAL_LIBRARY/DRUMS/SNARE/CLAP/house clap 4.wav",
    "./data/SAMPLES/ACTUAL_LIBRARY/DRUMS/SNARE/CLAP/multiclap.wav",
]


matches = []
for root, dirnames, filenames in os.walk("./data/SAMPLES/", followlinks=True):
    for filename in fnmatch.filter(filenames, "*.wav"):
        matches.append(os.path.join(root, filename))

print(matches)

# audio_embed = model.get_audio_embedding_from_filelist(x=audio_file, use_tensor=False)
# print(audio_embed[:, -20:])
# print(audio_embed.shape)
