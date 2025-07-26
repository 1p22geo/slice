from slice_backend.tags.tag import Tag


tags = [
    Tag("SLICE:DRUMS:RIM", "Rimshot", lambda name: "rim" in name.lower()),
    Tag("SLICE:DRUMS:SNARE", "Snare", lambda name: "snare" in name.lower()),
    Tag("SLICE:DRUMS:CLAP", "Clap", lambda name: "clap" in name.lower()),
    Tag("SLICE:DRUMS:KICK", "Kick", lambda name: "kick" in name.lower()),
    Tag(
        "SLICE:DRUMS:HH",
        "Hi-hat",
        lambda name: "hihat" in name.lower()
        or "hh" in name.lower()
        or "hi-hat" in name.lower(),
    ),
    Tag(
        "SLICE:DRUMS:HH:OPEN",
        "Open Hi-hat",
        lambda name: "open hat" in name.lower() or "open hihat" in name.lower(),
    ),
    Tag(
        "SLICE:DRUMS:HH:CLOSED",
        "Closed Hi-hat",
        lambda name: "closed hat" in name.lower() or "closed hihat" in name.lower(),
    ),
    Tag(
        "SLICE:DRUMS:CYMBALS",
        "Cymbals",
        lambda name: "cymbal" in name.lower()
        or "ride" in name.lower()
        or "crash" in name.lower(),
    ),
    Tag("SLICE:DRUMS:CYMBALS:RIDE", "Ride cymbal", lambda name: "ride" in name.lower()),
    Tag(
        "SLICE:DRUMS:CYMBALS:CRASH",
        "Crash cymbal",
        lambda name: "crash" in name.lower(),
    ),
]
