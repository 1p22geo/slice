from slice_backend.tags.tag import Tag


tags = [
    Tag(
        "SLICE:INSTRUM:PIANO",
        "Piano",
        lambda abs_path, sample_dir: "piano"
        in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:INSTRUM:GUITAR",
        "Guitar",
        lambda abs_path, sample_dir: "guit" in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:INSTRUM:STRINGS",
        "Strings",
        lambda abs_path, sample_dir: "string"
        in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:INSTRUM:VIBRAPHONE",
        "Vibraphone",
        lambda abs_path, sample_dir: "vibra"
        in abs_path.replace(sample_dir, "").lower(),
    ),
    Tag(
        "SLICE:INSTRUM:XYLOPHONE",
        "xylophonne",
        lambda abs_path, sample_dir: "xylo" in abs_path.replace(sample_dir, "").lower(),
    ),
]
