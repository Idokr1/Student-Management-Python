from sqlalchemy import text

from app.main import db

def get_json_value(x):
    if 'date' in  str(type(x)):
        return str(x)
    elif 'Decimal' in  str(type(x)):
        return float(x)
    return x

def get_paginated(fields, from_str, where_str, orderby_field, orderby_direction, page, count, params ):
    select_str = 'select ' + ','.join(map(lambda x: x[0] + " " + x[1] ,fields)) + ' ' + from_str + ' '
    ob = list(filter(lambda x: x[1] == orderby_field, fields))
    orderby_str = ""
    if (len(ob) > 0):
        orderby_str = " order by " + ob[0][0] + " " + orderby_direction + " "

    if page and  count:
        orderby_str = orderby_str + " limit " +str(count)
        orderby_str = orderby_str + " offset " + str((page - 1) * count)

    sql = select_str + where_str + orderby_str
    print("running:" + sql)
    fetchall = db.session.execute(text(sql), params).fetchall()
    rowcount = db.session.execute(text("select count(*) cnt from (" + select_str + where_str + ") as a"), params).fetchall()

    res = {}
    total = rowcount[0]["cnt"]
    res['count'] = total
    if count > total:
        count = total
    if page and count:
        res['page'] = page
        last = 1
        if total % count == 0:
            last = 0
        res['of_page'] = (total / count) + last
    res['data'] =  [dict(zip(row._fields, map(lambda x: get_json_value(x), row._data))) for row in fetchall]
    return res