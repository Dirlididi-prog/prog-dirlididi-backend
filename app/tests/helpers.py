from pytest import fixture

@fixture
def clear_db_data():
    from db import db
    db.session.remove()
    meta = db.metadata
    print(meta.sorted_tables)
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()