from slice_backend.tags.tag import Tag


tags = [
    Tag("SLICE:INSTRUM:PIANO", "Piano", lambda name: "piano" in name.lower()),
    Tag("SLICE:INSTRUM:GUITAR", "Guitar", lambda name: "guit" in name.lower()),
    Tag("SLICE:INSTRUM:STRINGS", "Strings", lambda name: "string" in name.lower()),
    Tag("SLICE:INSTRUM:VIBRAPHONE", "Vibraphone", lambda name: "vibra" in name.lower()),
    Tag("SLICE:INSTRUM:XYLOPHONE", "xylophonne", lambda name: "xylo" in name.lower()),
]
