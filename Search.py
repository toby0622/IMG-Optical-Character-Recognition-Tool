from PyZ3950 import zoom


def retrieve_z3950(cover_title):
    conn = zoom.Connection('metadata.ncl.edu.tw', 210)
    conn.databaseName = 'bg'
    conn.preferredRecordSyntax = 'MARC 21'
    conn.charset = "UTF-8"

    query = zoom.Query('CCL', str(cover_title))
    result = conn.search(query)

    for r in result:
        print(r)

    conn.close()
