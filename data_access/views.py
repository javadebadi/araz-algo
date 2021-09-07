from .da import engine

v_watch_list = \
"""
DROP VIEW v_watch_list;
CREATE VIEW v_watch_list AS
SELECT symbol
FROM symbol
JOIN watch_list
USING (symbol)"""

SQL_views = [v_watch_list]

def create_views():
    for view in SQL_views:
        with engine.begin() as con:
            stmts = view.split(';')
            for stmt in stmts:
                con.execute(stmt)