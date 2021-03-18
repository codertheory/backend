from codertheory.utils.ws_utils import EventsEnum


class PollEvents(EventsEnum):
    Connect = "connect"
    Disconnect = "disconnect"
    PollCreated = "poll_created"
    PollDeleted = "poll_deleted"
    PollVote = "poll_vote"
