from . import api


@api.route('/admin')
async def admin():

    return 'This is the admin page.'
