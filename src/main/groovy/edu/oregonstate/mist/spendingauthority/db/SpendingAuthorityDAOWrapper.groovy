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
        new ResultObject(data: getResourceObject(onid) ?: [])
    }

    private ResourceObject getResourceObject(String onid) {
        // Query expects onid in upper case
        String upperCaseOnid = onid.toUpperCase()

        // Queues for approvers. Approvers are tied to queues, which are tied to indexes.
        List<SpendingLimit> spendingLimits = spendingAuthorityDAO.getQueues(upperCaseOnid)

        // Indexes for requestors. Requestors have one spending limit.
        List<String> requestorIndexes = spendingAuthorityDAO.getRequestorIndexes(upperCaseOnid)

        if (!spendingLimits && !requestorIndexes) {
            return null
        }

        def limitsMap = [:]

        if (spendingLimits) {
            spendingLimits?.each {
                mapSpendingLimits(limitsMap,
                        it.queueLimit,
                        spendingAuthorityDAO.getIndexes(it.queueID))
            }
        }

        if (requestorIndexes) {
            mapSpendingLimits(limitsMap, requestorLimit, requestorIndexes)
        }

        // Reverse the map so we can key on the limit to get a list of indexes
        def spendingLimitsGroupedByLimit = limitsMap.groupEntriesBy { it.value }.each {
            it.value = it.value.collect { it.key }
        }

        new ResourceObject(
                id: upperCaseOnid,
                type: "spendingauthority",
                attributes: new Attributes(
                        limits: spendingLimitsGroupedByLimit.collect {
                            new LimitsForIndexes(spendingLimit: it.key, indexes: it.value)
                        }
                )
        )
    }

    private void mapSpendingLimits(def limitsMap, BigDecimal limit, List<String> indexes) {
        indexes.each {
            if (!limitsMap[it] || limitsMap[it] < limit) {
                limitsMap[it] = limit
            }
        }
    }
}
