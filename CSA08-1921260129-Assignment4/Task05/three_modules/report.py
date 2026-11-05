from pathlib import Path

def write_reports(percentages, absent, output_dir):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    (out / 'attendance_percentages.txt').write_text(str(percentages), encoding='utf-8')
    (out / 'absent_three_days.txt').write_text('\n'.join(absent), encoding='utf-8')
