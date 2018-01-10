package edu.oregonstate.mist.spendingauthority

import edu.oregonstate.mist.contrib.AbstractSpendingAuthorityDAO
import org.skife.jdbi.v2.sqlobject.Bind
import org.skife.jdbi.v2.sqlobject.SqlQuery
import org.skife.jdbi.v2.sqlobject.customizers.Mapper
import org.skife.jdbi.v2.sqlobject.customizers.RegisterMapper

public interface SpendingAuthorityDAO extends Closeable {
    @SqlQuery("SELECT 1 FROM dual")
    Integer checkHealth()

    @SqlQuery(AbstractSpendingAuthorityDAO.indexQuery)
    List<String> getIndexes(@Bind("queue_id") String queueID)

}
