from app.constants.dean import API


def get_ecard_balance(sess, student_id):
    """传入 requests 的 session
    """

    res = sess.get(API.card_data.format(student_id), verify=False)
    json = _parse_credit_progress(res.text)

    return json


def _parse_credit_progress(json):
    return json
