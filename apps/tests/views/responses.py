def success_response(data=None):
    return {
        'success': True,
        'data': data or {}
    }
