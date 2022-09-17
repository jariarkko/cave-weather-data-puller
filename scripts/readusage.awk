BEGIN {
}

/^# Call as follows/ {
    next;
}

/^# *$/ {
    printf("\n");
    next;
}

/^# [A-Za-z0-9]/ {
    thisline=substr($0,3)
    printf("%s\n",thisline)
    next;
}

/^#   / {
    thisline=substr($0,3)
    printf("  %s\n",thisline)
    next;
}

/^import/ {
    exit(0);
}

END {
}
