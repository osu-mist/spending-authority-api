package edu.oregonstate.mist.spendingauthority

import org.skife.jdbi.v2.StatementContext
import org.skife.jdbi.v2.tweak.ResultSetMapper

import java.sql.ResultSet
import java.sql.SQLException

public class SpendingAuthorityMapper implements ResultSetMapper<SpendingLimit> {
    public SpendingLimit map(int i, ResultSet rs, StatementContext sc) throws SQLException {
        new SpendingLimit (
                queueID: rs.getString("QUEUE_ID"),
                queueLimit: rs.getBigDecimal("QUEUE_LIMIT")
        )
    }
}
