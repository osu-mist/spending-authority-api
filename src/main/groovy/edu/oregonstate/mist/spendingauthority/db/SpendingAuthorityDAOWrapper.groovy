package edu.oregonstate.mist.spendingauthority.db

import edu.oregonstate.mist.api.jsonapi.ResourceObject
import edu.oregonstate.mist.api.jsonapi.ResultObject
import edu.oregonstate.mist.spendingauthority.Attributes
import edu.oregonstate.mist.spendingauthority.LimitsForIndexes
import edu.oregonstate.mist.spendingauthority.SpendingLimit

class SpendingAuthorityDAOWrapper {
    private final SpendingAuthorityDAO spendingAuthorityDAO

    private final BigDecimal requestorLimit = 4999.99

    SpendingAuthorityDAOWrapper(SpendingAuthorityDAO spendingAuthorityDAO) {
        this.spendingAuthorityDAO = spendingAuthorityDAO
    }

    public ResultObject getSpendingLimits(String onid) {
        new ResultObject(data: getResourceObject(onid))
    }

    private ResourceObject getResourceObject(String onid) {
        // Query expects onid in upper case
        String upperCaseOnid = onid.toUpperCase()

        // Queues for approvers. Approvers are tied to queues, which are tied to indexes.
        List<SpendingLimit> spendingLimits = spendingAuthorityDAO.getQueues(upperCaseOnid)

        // Indexes for requestors. Requestors have one spending limit.
        List<String> requestorIndexes = spendingAuthorityDAO.getRequestorIndexes(upperCaseOnid)

        List<LimitsForIndexes> limitsForIndexes = []

        if (spendingLimits) {
            spendingLimits.each {
                limitsForIndexes.add(new LimitsForIndexes(
                        spendingLimit: it.queueLimit,
                        indexes: spendingAuthorityDAO.getIndexes(it.queueID)))
            }
        }

        if (requestorIndexes) {
            limitsForIndexes.add(new LimitsForIndexes(
                    spendingLimit: requestorLimit,
                    indexes: requestorIndexes))
        }

        if (limitsForIndexes) {
            return new ResourceObject(
                    id: upperCaseOnid,
                    type: "spendingauthority",
                    attributes: new Attributes(
                            limits: limitsForIndexes
                    )
            )
        } else {
            return null
        }
    }

}
