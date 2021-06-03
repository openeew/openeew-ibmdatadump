class Detections:
    """This dataclass holds a reference to the Detections DF in memory."""

    # print("✅ Created empty list for detections.")
    # data: list = field(default_factory=list)
    # print(data.default_factory)

    def __init__(self):
        self.data = []


class Events:
    """This dataclass holds a reference to the Events DF in memory."""

    # print("✅ Created empty list for events.")
    # data: list = field(default_factory=list)

    def __init__(self):
        self.data = []
