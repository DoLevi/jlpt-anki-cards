# jlpt-anki-cards

## Aim
Generate anki cards with
* a vocabulary list
* pitch information from `https://takoboto.jp/?q` (see below)
* chatbot to sort cards according to categories

## Anki cards
### Field explanations
Target Word
* in vocabulary list

Reading
* in vocabulary list

Pitch Accent
* tbd by learner

Pitch Peak (xw / xs)
* x <- index of syllable with border-right (1..n)
* w <- if no border-right is on the reading-`span`
* s <- if border-right is on the reading-`span`

Definition
* in vocabulary list

### Export example
Located in directory `examples/`.

