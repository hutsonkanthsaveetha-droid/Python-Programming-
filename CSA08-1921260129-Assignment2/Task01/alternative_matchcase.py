def match_case_decision(units, ration_card, member_over_80):
    match units:
        case value if value <= 100:
            return "Full subsidy"
        case value if 101 <= value <= 200 and ration_card:
            return "Partial subsidy"
        case value if value > 200 and member_over_80:
            return "Senior exception subsidy"
        case _:
            return "No subsidy"


if __name__ == "__main__":
    cases = [(100, True, False), (101, True, False), (201, False, True)]
    for units, ration, senior in cases:
        print(units, ration, senior, "->", match_case_decision(units, ration, senior))
