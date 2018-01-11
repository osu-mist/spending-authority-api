package edu.oregonstate.mist.spendingauthority.db

import edu.oregonstate.mist.api.jsonapi.ResourceObject
import edu.oregonstate.mist.api.jsonapi.ResultObject
import edu.oregonstate.mist.spendingauthority.Attributes
import edu.oregonstate.mist.spendingauthority.LimitsForIndexes
import edu.oregonstate.mist.spendingauthority.SpendingLimit

class SpendingAuthorityDAOWrapper {
    private final SpendingAuthorityDAO spendingAuthorityDAO

    SpendingAuthorityDAOWrapper(SpendingAuthorityDAO spendingAuthorityDAO) {
        this.spendingAuthorityDAO = spendingAuthorityDAO
    }

    public ResultObject getSpendingLimits(String onid) {
        new ResultObject(
                data: getResourceObject(onid)
        )
    }

    private ResourceObject getResourceObject(String onid) {
        String upperCaseOnid = onid.toUpperCase()
        List<SpendingLimit> spendingLimits = spendingAuthorityDAO.getQueues(upperCaseOnid)

        List<LimitsForIndexes> limitsForIndexes = []

        spendingLimits.each {
            limitsForIndexes.add(new LimitsForIndexes(
                    spendingLimit: it.queueLimit,
                    indexes: spendingAuthorityDAO.getIndexes(it.queueID)))
        }

        new ResourceObject(
                id: upperCaseOnid,
                attributes: new Attributes(
                        limits: limitsForIndexes
                )
        )
    }

}
