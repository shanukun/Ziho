from flask_sqlalchemy.pagination import SelectPagination


def paginate(db, select, page, per_page, error_out=True):
    return ZihoPagination(
        select=select,
        session=db.session(),
        page=page,
        per_page=per_page,
        error_out=error_out,
    )


# This is workaround for a issue in flask_sqlalchemy.pagination.
# https://github.com/pallets-eco/flask-sqlalchemy/issues/1168
class ZihoPagination(SelectPagination):

    def _query_items(self):
        select = self._query_args["select"]
        select = select.limit(self.per_page).offset(self._query_offset)
        session = self._query_args["session"]

        # Change from SelectPagination
        # return list(session.execute(select).unique().scalars())
        return list(session.execute(select).unique().all())
