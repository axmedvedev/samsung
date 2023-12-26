from config import *

def serializer(data):
    try:
        if not data:
            return []

        if isinstance(data, (bool, str, int, float, type(None))):
            return data

        if isinstance(data, list):
            result = []
            for item in data:
                result.append(serializer(item))
            return result

        try:
            return {key: value for key, value in data.__dict__.items() if not key.startswith('_')}
        except:
            result = {}
            for key, value in data._asdict().items():
                if not isinstance(value, (bool, str, int, float, type(None))):
                    result.update(serializer(value))
                else:
                    result.update({key: value})
            return result

    except Exception as e:
        logging.error(e)
        return []


def compileData(rows):
    compiled_rows = []
    for row in rows:
        current_row = next((item for item in compiled_rows if row['id'] == item['id']), None)
        if current_row is None:
            image = [row['image_name']] if row['image_name'] is not None else []
            row.update({'carousel': image})
            row.pop('image_name')
            compiled_rows.append(row)
        else:
            if row['image_name'] is not None:
                current_row['carousel'].append(row['image_name'])
    return compiled_rows