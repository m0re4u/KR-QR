# KR-QR

## Requirements
### Python packages
- [networkx](https://networkx.github.io/)
- [graphviz](https://pypi.python.org/pypi/graphviz)

### Programs
- [graphviz](http://www.graphviz.org/)

## Generating the state graph and transitions
```bash
python3 main.py [-f OUTFILE]
```
This command generated a file that contains all the states, and the possible transitions between them. The file can in turn be used in any visualization program, one of which is included in this repository.

## Generating a visualization of the state graph
```bash
python3 graph_states [-f INFILE]
```
The visualization of the state graph uses graphviz.
