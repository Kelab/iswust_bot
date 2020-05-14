from apscheduler.jobstores.base import ConflictingIdError


class SchedulerError(Exception):
    pass


class JobIdConflictError(ConflictingIdError, SchedulerError):
    pass
