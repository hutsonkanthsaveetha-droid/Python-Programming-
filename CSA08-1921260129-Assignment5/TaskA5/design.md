# A5 - Citizen complaint AI design

## Lexicon sentiment
Tokenise text into lower-case words. Give +1 to positive words and -1 to negative words; if the immediately preceding word is a negator (`not`, `never`, `no`, `hardly`), flip the current word's sign. The sign of the total determines positive, negative or neutral. This is transparent and fast but does not reliably understand sarcasm, scope beyond one preceding word, double negation, domain context or mixed opinion.

## Extractive summary
Split a complaint into sentences, count important words after stop-word removal, score each sentence by the frequencies of its important words, and return the top k in original order. It reuses original sentences and does not invent text, but it may miss context or select redundant sentences.

## Rule-based chatbot
Match a question containing `PM2.5` and `in <station>`; query the SQLite readings table using a `?` parameter and the latest date in the dataset. Unknown stations/questions receive a safe clarification. Limitations: fixed wording, no multi-turn context, no location disambiguation, latest available data may not be live, averages hide local/hourly variation, no language understanding or explanation of health risk.

## Alternative: trained model
A Naive Bayes model requires labelled complaint data and feature extraction; inference is often O(number of features) per complaint and model memory is proportional to vocabulary/classes. A pre-trained language model can capture context/sarcasm better but uses far more memory and compute and may require network/GPU resources. A lexicon is explainable, tiny and fast; a trained model may improve accuracy on local language but must be evaluated on representative labelled complaints and monitored for drift.


## Alternative: first-k sentence baseline
A baseline can return the first k complaint sentences without calculating word frequencies. For a fixed k this selection is O(1) with respect to the corpus length after the first k records are available, and it needs O(1) extra working space aside from the returned text. Frequency-based extraction scans/scorers W words (O(W)) and keeps word/sentence counts (O(V + S) space). The sample comparison is recorded in TaskB4: the first-five baseline covers 13 of the top 15 important corpus terms (86.7%), while the frequency selection covers 9 of 15 (60.0%). On this particular prepared dataset the first-five selection happens to cover more top terms; the result shows that extractive ranking must be evaluated on the actual corpus rather than assumed to be better.
