package edu.oregonstate.mist.spendingauthority

class Attributes {
    List<LimitsForIndexes> limits
}

class LimitsForIndexes {
    BigDecimal spendingLimit
    List<String> indexes
}

class SpendingLimit {
    String queueID
    BigDecimal queueLimit
}