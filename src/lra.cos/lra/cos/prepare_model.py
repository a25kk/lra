# -*- coding: utf-8 -*-
"""Module providing database setup"""


def prepare(engine):
    from lra.cos import ORMBase
    from sqlalchemy.exc import OperationalError
    # Bind SQLALchemy engine
    try:
        import lra.cos.appointments
        import lra.cos.consultationslots
        ORMBase.metadata.create_all(engine)
    except OperationalError:
        import pdb; pdb.set_trace()
        pass
