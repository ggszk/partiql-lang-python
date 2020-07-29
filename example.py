from lark import Lark
from partiql_lang import Build_AST

samples = [
    "SELECT p FROM Person AS p",
    "SELECT Person FROM Person",
    "SELECT jenn.name, jenn.name FROM Person AS jenn",
    "SELECT jenn FROM Person AS jenn WHERE jenn.name = 'Jennifer'",
    "SELECT company.name FROM Person AS p, p.WORKS_FOR AS company WHERE p.name = 'Jennifer'",
    "SELECT Person, Person.name FROM Person",
    "SELECT from_node.n_id, dijkstra(from_node, to_node, 'CONNECT_TO', 'cost'), to_node.n_id FROM g2 AS from_node, g2 AS to_node WHERE from_node.n_id = 0 AND to_node.n_id = 8",
    "SELECT add(col1, col2) FROM table3",
    "SELECT p1.name FROM Person AS p1",
]

rule = open('partiql_grammer.lark').read()
parser = Lark(rule, start="select", parser='lalr')

for sample in samples :
    tree = parser.parse(sample)
    print(tree)
    b = Build_AST()
    ast = b.visit(tree)
    print(ast)

