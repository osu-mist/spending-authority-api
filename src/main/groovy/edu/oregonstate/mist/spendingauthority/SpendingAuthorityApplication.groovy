package edu.oregonstate.mist.spendingauthority

import edu.oregonstate.mist.api.Application
import edu.oregonstate.mist.spendingauthority.db.SpendingAuthorityDAO
import edu.oregonstate.mist.spendingauthority.db.SpendingAuthorityDAOWrapper
import io.dropwizard.jdbi.DBIFactory
import io.dropwizard.setup.Environment
import org.skife.jdbi.v2.DBI

/**
 * Main application class.
 */
class SpendingAuthorityApplication extends Application<SpendingAuthorityConfiguration> {
    /**
     * Parses command-line arguments and runs the application.
     *
     * @param configuration
     * @param environment
     */
    @Override
    public void run(SpendingAuthorityConfiguration configuration, Environment environment) {
        this.setup(configuration, environment)

        DBIFactory factory = new DBIFactory()
        DBI jdbi = factory.build(environment, configuration.getDataSourceFactory(), "jdbi")
        SpendingAuthorityDAO spendingAuthorityDAO = jdbi.onDemand(SpendingAuthorityDAO.class)
        SpendingAuthorityDAOWrapper spendingAuthorityDAOWrapper = new SpendingAuthorityDAOWrapper(
                spendingAuthorityDAO
        )
        environment.jersey().register(new SpendingAuthorityResource(spendingAuthorityDAOWrapper))

        SpendingAuthorityHealthCheck healthCheck = new SpendingAuthorityHealthCheck(
                spendingAuthorityDAO)
        environment.healthChecks().register("spendingAuthorityHealthCheck", healthCheck)
    }

    /**
     * Instantiates the application class with command-line arguments.
     *
     * @param arguments
     * @throws Exception
     */
    public static void main(String[] arguments) throws Exception {
        new SpendingAuthorityApplication().run(arguments)
    }
}
