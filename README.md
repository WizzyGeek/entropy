# Entropy

See the informational entropy of a file (assuming the encoded symbols are bytes or bits)
This doesn't necessarily give the best possible compression, as for certain data, it is possible
to identify bit sequences as symbols such that it minimises the entropy.

Here we assume that a byte is the only symbol encoded and output the entropy which
can reflect accurately the compression ratios possible for byte level compression algorithms


```
python3 entropy.py source.txt
```