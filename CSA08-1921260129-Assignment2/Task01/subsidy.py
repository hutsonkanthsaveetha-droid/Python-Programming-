from dataclasses import dataclass

@dataclass(frozen=True)
class Household:
    name: str
    units: int
    ration_card: bool
    member_over_80: bool


def separate_if_decision(units, ration_card, member_over_80):
    decisions = []
    if units <= 100:
        decisions.append("Full subsidy")
    if 101 <= units <= 200 and ration_card:
        decisions.append("Partial subsidy")
    if units > 200:
        if member_over_80:
            decisions.append("Senior exception subsidy")
        else:
            decisions.append("No subsidy")
    if not decisions:
        decisions.append("No subsidy")
    return decisions


def elif_decision(units, ration_card, member_over_80):
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200 and ration_card:
        return "Partial subsidy"
    elif units > 200 and member_over_80:
        return "Senior exception subsidy"
    else:
        return "No subsidy"


def overlapping_if_example(units, ration_card):
    decisions = []
    if units <= 100:
        decisions.append("Full subsidy")
    if units <= 200 and ration_card:
        decisions.append("Partial subsidy")
    return decisions


HOUSEHOLDS = [
    Household("H1", 50, False, False),
    Household("H2", 100, True, False),
    Household("H3", 101, False, False),
    Household("H4", 101, True, False),
    Household("H5", 200, True, False),
    Household("H6", 200, False, True),
    Household("H7", 201, False, False),
    Household("H8", 201, False, True),
]


def main():
    print("Household | Units | Ration | Age >80 | separate-if | if-elif-else")
    for h in HOUSEHOLDS:
        separate = "; ".join(separate_if_decision(h.units, h.ration_card, h.member_over_80))
        chained = elif_decision(h.units, h.ration_card, h.member_over_80)
        print(f"{h.name:9} | {h.units:5} | {str(h.ration_card):6} | {str(h.member_over_80):7} | {separate:25} | {chained}")
    print("Overlap example (80 units + ration card):", overlapping_if_example(80, True))

if __name__ == "__main__":
    main()
