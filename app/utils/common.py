from quart import abort


def trueRet(data="NULL", msg="success"):
    return {"code": 200, "data": data, "msg": msg}


def falseRet(data="NULL", msg="fail", code=-1):
    return {"code": code, "data": data, "msg": msg}


def abort_if_qq_doesnt_exist(qq):
    abort(404, message="Todo {} doesn't exist".format(qq))
