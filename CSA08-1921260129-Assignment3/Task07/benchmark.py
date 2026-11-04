import csv
import random
import time
from pathlib import Path
from Task07.contact_merge import merge_contacts, normalise_number


def generate(n, seed=707):
    rng = random.Random(seed + n)
    sources = {'phone_a': [], 'phone_b': [], 'sim': []}
    for i in range(n):
        person = i // 2
        phone = f'98400{person:05d}'
        if i % 2:
            phone = '+91 ' + phone[:5] + ' ' + phone[5:]
        source = ('phone_a', 'phone_b', 'sim')[i % 3]
        sources[source].append({'name': f'Person {person}', 'phones': [phone], 'emails': [f'p{person}@example.com'] if rng.random() > 0.1 else []})
    return sources


def timed(fn):
    start=time.perf_counter(); result=fn(); return time.perf_counter()-start, result


def pairwise_duplicate_keys(contacts):
    keys=[]
    for group in contacts.values():
        for contact in group:
            phone=contact.get('phones',[])
            if isinstance(phone,str): phone=[phone]
            if phone: keys.append(normalise_number(phone[0]))
    duplicate_pairs=0
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            if keys[i] == keys[j]: duplicate_pairs += 1
    return duplicate_pairs


def main():
    rows=[]
    for n in (1_000,100_000):
        sources=generate(n)
        elapsed, merged=timed(lambda: merge_contacts(sources))
        rows.append((n, elapsed, len(merged)))
        print(f'contacts={n:>6} dictionary_merge={elapsed:.6f}s merged_groups={len(merged)}')
    small=generate(1_000)
    pair_time, pairs=timed(lambda: pairwise_duplicate_keys(small))
    print(f'pairwise alternative measured at 1,000 inputs: {pair_time:.6f}s; matching pairs={pairs}')
    estimated_100k=pair_time * ((100_000*99_999)/(1_000*999))
    print(f'pairwise 100,000 estimate (quadratic scaling, NOT measured): {estimated_100k:.2f}s')
    out=Path(__file__).parent/'outputs'/'contact_benchmark.csv'; out.parent.mkdir(exist_ok=True)
    with open(out,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['input_contacts','dictionary_merge_seconds','merged_groups']); w.writerows(rows)
    with open(Path(__file__).parent/'outputs'/'pairwise_alternative.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['input_contacts','measured_or_estimated_seconds','status']); w.writerow([1_000,pair_time,'measured']); w.writerow([100_000,estimated_100k,'estimated from quadratic scaling; not run'])


if __name__=='__main__': main()
