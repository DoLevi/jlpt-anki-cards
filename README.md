# jlpt-anki-cards

## Aim
Generate anki cards with
* a vocabulary list https://www.kanshudo.com/collections/wikipedia\_jlpt
* ~~pitch information from `https://takoboto.jp/?q` (see below)~~
* ~~chatbot to sort cards according to categories~~

## Anki cards
### Field explanations
Target Word
* in vocabulary list in target language

Reading
* in vocabulary list in target language

Sentence
* in vocabulary list in target language

Pitch Accent
* documented by learner

Pitch Peak (xw / xs)
* x <- index of syllable with border-right (1..n)
* w <- if no border-right is on the reading-`span`
* s <- if border-right is on the reading-`span`

Definition
* in vocabulary list (just take all verbatim)

Tag
* `(jp)vocab\_n5..1`

### Export example
Located in directory `examples/`.

