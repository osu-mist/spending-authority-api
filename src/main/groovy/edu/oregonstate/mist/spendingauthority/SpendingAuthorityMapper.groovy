package edu.oregonstate.mist.spendingauthority

import edu.oregonstate.mist.api.jsonapi.ResourceObject
import org.skife.jdbi.v2.StatementContext
import org.skife.jdbi.v2.tweak.ResultSetMapper

import java.sql.ResultSet
import java.sql.SQLException

public class SpendingAuthorityMapper implements ResultSetMapper<ResourceObject> {

    public ResourceObject map(int i, ResultSet rs, StatementContext sc) throws SQLException {
        new ResourceObject(
                id: rs.getString("OSUUID"),
                type: "person",
                attributes: "blah",
                links: ["related": rs.getString("OSUUID")]
        )
    }
}
