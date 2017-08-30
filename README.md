# propositional-theorem-prover
An automated theorem prover, no optimization currently.

## Usage

    python -m prover "SEQUENT"

## Format

The input will consist of a single [sequent](https://www.wikiwand.com/en/Sequent_calculus) of the command line.

    SEQUENT -> [List of FORMULA] seq [List of FORMULA]
    FORMULA -> ATOM | (FORMULA) | neg FORMULA | FORMULA and FORMULA | FORMULA or FORMULA | FORMULA imp FORMULA | FORMULA iff FORMULA
    ATOM    -> [a-z]+

## Examples

    python -m prover "[p imp q, (neg r) imp (neg q)] seq [p imp r]"

    Output:
    0: [(p imp q), ((neg r) imp (neg q))] seq [(p imp r)], by rule P5b -> (4, 5)
    4: [(p imp q), (neg q)] seq [(p imp r)], by rule P5b -> (18, 19)
    18: [(neg q), q] seq [(p imp r)], by rule P2b -> 48
    48: [q] seq [(p imp r), q], by rule P1  -> true
    19: [(neg q)] seq [(p imp r), p], by rule P5a -> 51
    51: [(neg q), p] seq [p, r], by rule P1  -> true
    5: [(p imp q)] seq [(p imp r), (neg r)], by rule P2a -> 20
    20: [(p imp q), r] seq [(p imp r)], by rule P5a -> 52
    52: [(p imp q), r, p] seq [r], by rule P1  -> true
    QED
    True