package edu.oregonstate.mist.spendingauthority

import com.codahale.metrics.health.HealthCheck
import com.codahale.metrics.health.HealthCheck.Result

class SpendingAuthorityHealthCheck extends HealthCheck {
    private SpendingAuthorityDAO spendingAuthorityDAO

    SpendingAuthorityHealthCheck(SpendingAuthorityDAO spendingAuthorityDAO) {
        this.spendingAuthorityDAO = spendingAuthorityDAO
    }

    @Override
    protected Result check() {
        try {
            String status = spendingAuthorityDAO.checkHealth()

            if (status != null) {
                return Result.healthy()
            }
            Result.unhealthy("status: ${status}")
        } catch(Exception e) {
            Result.unhealthy(e.message)
        }
    }
}
