from slice_backend.tags.tag import Tag


tags = [
    Tag(
        "SLICE:FX",
        "SFX",
        lambda abs_path, sample_dir: "fx" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:FX:AMBIENC",
        "Ambience",
        lambda abs_path, sample_dir: "drone" in abs_path.replace(sample_dir, "").lower()
        or "ambience" in abs_path.replace(sample_dir, "").lower()
        or "atmos" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:FX:RISER",
        "Riser",
        lambda abs_path, sample_dir: "riser"
        in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:FX:DOWNLIFTER",
        "Downlifter",
        lambda abs_path, sample_dir: "downlifter"
        in abs_path.replace(sample_dir, "").lower()
        or "white noise down" in abs_path.replace(sample_dir, "").lower()
        or "downleafter"
        in abs_path.replace(sample_dir, "").lower(),  # my sample library is a mess
    ),
]
