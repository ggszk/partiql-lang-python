import pytest

from lark import Lark
from partiql_lang import Build_AST

# test pattern
# samples of Query and AST
# Remark: we don't fully parse for simple translation.
@pytest.mark.parametrize(('query', 'ast'), [
    (
        "SELECT p FROM Person AS p",
        ['select', ['project', ['list', ['id', 'p']]], ['from', ['as', 'p', ['id', 'Person']]]]
    ),
    (
        "SELECT Person FROM Person",
        ['select', ['project', ['list', ['id', 'Person']]], ['from', ['as', 'Person', ['id', 'Person']]]]
    ),
    (
        "SELECT jenn.name, jenn.name FROM Person AS jenn",
        ['select', ['project', ['list', ['path', ['id', 'jenn'], ['id', 'name']], ['path', ['id', 'jenn'], ['id', 'name']]]], ['from', ['as', 'jenn', ['id', 'Person']]]]
    ),
    (
        "SELECT jenn FROM Person AS jenn WHERE jenn.name = 'Jennifer'",
        ['select', ['project', ['list', ['id', 'jenn']]], ['from', ['as', 'jenn', ['id', 'Person']]], ['where', ['=', ['path', ['id', 'jenn'], ['id', 'name']], ['lit', "'Jennifer'"]]]]
    ),
    (
        "SELECT company.name FROM Person AS p, p.WORKS_FOR AS company WHERE p.name = 'Jennifer'",
        ['select', 
            ['project', ['list', ['path', ['id', 'company'], ['id', 'name']]]], 
            ['from', 
                ['inner_join', 
                    ['as', 'p', ['id', 'Person']], 
                    ['as', 'company', ['path', ['id', 'p'], ['id', 'WORKS_FOR']]]
                ]
            ],
            ['where', ['=', ['path', ['id', 'p'], ['id', 'name']], ['lit', "'Jennifer'"]]]
        ]
    ),
    (
        "SELECT Person, Person.name FROM Person",
        ['select', ['project', ['list', ['id', 'Person'], ['path', ['id', 'Person'], ['id', 'name']]]], ['from', ['as', 'Person', ['id', 'Person']]]]
    ),
    (
        "SELECT from_node.n_id, dijkstra(from_node, to_node, 'CONNECT_TO', 'cost'), to_node.n_id FROM g2 AS from_node, g2 AS to_node WHERE from_node.n_id = 0 AND to_node.n_id = 8",
        ['select', 
            ['project', 
                ['list', 
                    ['path', ['id', 'from_node'], ['id', 'n_id']],
                    ['call', 'dijkstra', ['list', ['id', 'from_node'], ['id', 'to_node'], ['lit', "'CONNECT_TO'"], ['lit', "'cost'"]]],
                    ['path', ['id', 'to_node'], ['id', 'n_id']]
                ]
            ],
            ['from', 
                ['inner_join', 
                    ['as', 'from_node', ['id', 'g2']], 
                    ['as', 'to_node',  ['id', 'g2']]
                ]
            ],
            ['where', 
                ['and', 
                    ['=', ['path', ['id', 'from_node'], ['id', 'n_id']], ['lit', 0]], 
                    ['=', ['path', ['id', 'to_node'], ['id', 'n_id']], ['lit', 8]]
                ]
            ]
        ]
    )
])

def test_partiql_python(query, ast) :
    rule = open('partiql_grammer.lark').read()
    parser = Lark(rule, start="select", parser='lalr')

    b = Build_AST()
    tree = parser.parse(query)
    assert b.visit(tree) == ast



