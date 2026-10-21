from milkrate import BASE_RATE, REFERENCE_FAT, REFERENCE_SNF, FAT_STEP_VALUE, SNF_STEP_VALUE

print(f"Base rate: Rs {BASE_RATE:.2f}")
print(f"Reference fat: {REFERENCE_FAT}%")
print(f"Reference SNF: {REFERENCE_SNF}%")
print(f"Fat step value: Rs {FAT_STEP_VALUE:.2f}")
print(f"SNF step value: Rs {SNF_STEP_VALUE:.2f}")

first, second = 10, "10 litres"
print("Before reassignment:", type(first).__name__, type(second).__name__)
first, second = second, first
print("After swap:", first, second)
