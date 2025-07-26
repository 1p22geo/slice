from slice_backend.tags.tag import Tag


tags = [
    Tag(
        "SLICE:DRUMS",
        "Drums",
        lambda abs_path, sample_dir: "drum" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:PERC",
        "Percussion",
        lambda abs_path, sample_dir: "perc" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:RIM",
        "Rimshot",
        lambda abs_path, sample_dir: "rim" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:SNARE",
        "Snare",
        lambda abs_path, sample_dir: "snare"
        in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:TOM",
        "Tom",
        lambda abs_path, sample_dir: "tom" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:CLAP",
        "Clap",
        lambda abs_path, sample_dir: "clap" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:KICK",
        "Kick",
        lambda abs_path, sample_dir: "kick" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:HH",
        "Hi-hat",
        lambda abs_path, sample_dir: "hihat" in abs_path.replace(sample_dir, "").lower()
        or "hh" in abs_path.replace(sample_dir, "").lower()
        or "hi-hat" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:HH:OPEN",
        "Open Hi-hat",
        lambda abs_path, sample_dir: "open hat"
        in abs_path.replace(sample_dir, "").lower()
        or "open hihat" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:HH:CLOSED",
        "Closed Hi-hat",
        lambda abs_path, sample_dir: "closed hat"
        in abs_path.replace(sample_dir, "").lower()
        or "closed hihat" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:CYMBALS",
        "Cymbals",
        lambda abs_path, sample_dir: "cymbal"
        in abs_path.replace(sample_dir, "").lower()
        or "ride" in abs_path.replace(sample_dir, "").lower()
        or "crash" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:CYMBALS:RIDE",
        "Ride cymbal",
        lambda abs_path, sample_dir: "ride" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:DRUMS:CYMBALS:CRASH",
        "Crash cymbal",
        lambda abs_path, sample_dir: "crash"
        in abs_path.replace(sample_dir, "").lower(),
    ),
]
