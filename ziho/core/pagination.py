import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from flask_sqlalchemy.pagination import Pagination


def paginate(db, select, page, per_page, error_out=True):
    return ZihoPagination(
        select=select,
        session=db.session(),
        page=page,
        per_page=per_page,
        error_out=error_out,
    )


class ZihoPagination(Pagination):

    def _query_items(self):
        select = self._query_args["select"]
        select = select.limit(self.per_page).offset(self._query_offset)
        session = self._query_args["session"]
        return list(session.execute(select).unique().all())

    def _query_count(self) -> int:
        select = self._query_args["select"]
        sub = select.options(sa_orm.lazyload("*")).order_by(None).subquery()
        session = self._query_args["session"]
        out = session.execute(sa.select(sa.func.count()).select_from(sub)).scalar()
        return out  # type: ignore[no-any-return]
