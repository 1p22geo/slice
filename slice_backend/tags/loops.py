from slice_backend.tags.tag import Tag


tags = [
    Tag(
        "SLICE:LOOPS",
        "Loops",
        lambda abs_path, sample_dir: "loop" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:LOOPS:SHAKER",
        "Shaker Loops",
        lambda abs_path, sample_dir: "loop" in abs_path.replace(sample_dir, "").lower()
        and "shaker" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:LOOPS:HIHAT",
        "Hi-hat Loops",
        lambda abs_path, sample_dir: "loop" in abs_path.replace(sample_dir, "").lower()
        and (
            "hat" in abs_path.replace(sample_dir, "").lower()
            or "hh" in abs_path.replace(sample_dir, "").lower()
        ),
    ),
    Tag(
        "SLICE:LOOPS:FILLS",
        "Drum fills",
        lambda abs_path, sample_dir: "fill" in abs_path.replace(sample_dir, "").lower(),
    ),
]
