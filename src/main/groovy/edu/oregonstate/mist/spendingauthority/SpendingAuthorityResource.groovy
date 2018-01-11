package edu.oregonstate.mist.spendingauthority

import com.codahale.metrics.annotation.Timed
import edu.oregonstate.mist.api.Resource
import edu.oregonstate.mist.spendingauthority.db.SpendingAuthorityDAOWrapper
import groovy.transform.TypeChecked

import javax.annotation.security.PermitAll
import javax.ws.rs.GET
import javax.ws.rs.Path
import javax.ws.rs.Produces
import javax.ws.rs.QueryParam
import javax.ws.rs.core.MediaType
import javax.ws.rs.core.Response

@Path("spendingauthority")
@Produces(MediaType.APPLICATION_JSON)
@PermitAll
@TypeChecked
class SpendingAuthorityResource extends Resource {
    private final SpendingAuthorityDAOWrapper spendingAuthorityDAOWrapper

    SpendingAuthorityResource(SpendingAuthorityDAOWrapper spendingAuthorityDAOWrapper) {
        this.spendingAuthorityDAOWrapper = spendingAuthorityDAOWrapper
    }

    @Timed
    @GET
    Response getSpendingAuthority(@QueryParam('onid') String onid) {
        ok(spendingAuthorityDAOWrapper.getSpendingLimits(onid)).build()
    }
}
