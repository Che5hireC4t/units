from pickle import dumps, loads


def get_unpickled_pickled_copy(gizmo: object):
    """
    @gizmo      Any     Any python object

    @return     Any     A pickled-then-unpickled copy of @gizmo
    """
    pickled_gizmo = dumps(gizmo)
    return loads(pickled_gizmo)
