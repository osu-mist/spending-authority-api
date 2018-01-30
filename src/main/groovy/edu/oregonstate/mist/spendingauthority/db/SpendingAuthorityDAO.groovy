package edu.oregonstate.mist.spendingauthority.db

import edu.oregonstate.mist.contrib.AbstractSpendingAuthorityDAO
import edu.oregonstate.mist.spendingauthority.SpendingAuthorityMapper
import edu.oregonstate.mist.spendingauthority.SpendingLimit
import org.skife.jdbi.v2.sqlobject.Bind
import org.skife.jdbi.v2.sqlobject.SqlQuery
import org.skife.jdbi.v2.sqlobject.customizers.Mapper

public interface SpendingAuthorityDAO extends Closeable {
    @SqlQuery("SELECT 1 FROM dual")
    Integer checkHealth()

    @SqlQuery(AbstractSpendingAuthorityDAO.queueQuery)
    @Mapper(SpendingAuthorityMapper)
    List<SpendingLimit> getQueues(@Bind("onid") String onid)

    @SqlQuery(AbstractSpendingAuthorityDAO.indexQuery)
    List<String> getIndexes(@Bind("queueID") String queueID)

    @SqlQuery(AbstractSpendingAuthorityDAO.requestorQuery)
    List<String> getRequestorIndexes(@Bind("onid") String onid)

}
