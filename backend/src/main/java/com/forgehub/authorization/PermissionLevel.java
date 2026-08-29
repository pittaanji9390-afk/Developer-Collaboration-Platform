package com.forgehub.authorization;

public enum PermissionLevel {
    READ(1),
    TRIAGE(2),
    WRITE(3),
    MAINTAIN(4),
    ADMIN(5);

    private final int rank;

    PermissionLevel(int rank) {
        this.rank = rank;
    }

    public boolean includes(PermissionLevel required) {
        return this.rank >= required.rank;
    }
}
