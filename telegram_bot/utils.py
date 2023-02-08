def get_callback_query_data(query_data: str) -> str:
    _, *data = query_data.split(':')

    return ':'.join(data)
