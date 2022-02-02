class Angle:
    """
    The length of the "heading" values between two
    points gives the difference between the "heading".
    The values that remain above the parameter that,
    "header_limit" will be marked as an anomaly.
    """
    header_limit = 15

    def __init__(self):
        self.upper_angle = int
        self.lower_angle = int

    def rang(self, pair_head: list) -> int:
        self.upper_angle = int(max(pair_head[0], pair_head[1]))
        self.lower_angle = int(min(pair_head[0], pair_head[1]))
        range_angle = range(self.lower_angle, self.upper_angle)
        range_angle = [a % 360 if a >= 360 else a for a in range_angle]
        return len(range_angle)