import math

for fat in (4.2, 3.1):
    raw = (fat - 3.5) / 0.1
    print("fat:", fat, "raw:", raw, "round:", round(raw),
          "int:", int(raw), "floor:", math.floor(raw))

print("(4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)
print("0.1 + 0.2 =", 0.1 + 0.2)
print("round(2.675, 2) =", round(2.675, 2))
print("2.0 <= 4.2 <= 7.0 =", 2.0 <= 4.2 <= 7.0)
print("-7 // 2 =", -7 // 2, "; int(-7 / 2) =", int(-7 / 2))
