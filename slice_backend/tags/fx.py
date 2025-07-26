from slice_backend.tags.tag import Tag


tags = [
    Tag("SLICE:FX", "SFX", lambda name: "fx" in name.lower()),
    Tag(
        "SLICE:FX:AMBIENC",
        "Ambience",
        lambda name: "drone" in name.lower()
        or "ambience" in name.lower()
        or "atmos" in name.lower(),
    ),
    Tag("SLICE:FX:RISER", "Riser", lambda name: "riser" in name.lower()),
    Tag(
        "SLICE:FX:DOWNLIFTER",
        "Downlifter",
        lambda name: "downlifter" in name.lower()
        or "white noise down" in name.lower()
        or "downleafter" in name.lower(),  # my sample library is a mess
    ),
]
