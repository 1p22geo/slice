from slice_backend.tags.tag import Tag


tags = [
    Tag("SLICE:LOOPS", "Loops", lambda name: "loop" in name.lower()),
    Tag(
        "SLICE:LOOPS:SHAKER",
        "Shaker Loops",
        lambda name: "loop" in name.lower() and "shaker" in name.lower(),
    ),
    Tag(
        "SLICE:LOOPS:HIHAT",
        "Hi-hat Loops",
        lambda name: "loop" in name.lower()
        and ("hat" in name.lower() or "hh" in name.lower()),
    ),
    Tag("SLICE:LOOPS:FILLS", "Drum fills", lambda name: "fill" in name.lower()),
]
