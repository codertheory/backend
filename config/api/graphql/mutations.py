import graphene
from graphql_auth import relay as mutations

from codertheory.polls.graphql.mutations import *
from codertheory.projects.graphql.mutations import *
from codertheory.shiritori.graphql.mutations import *

__all__ = (
    "Mutations",
)


class Mutations(graphene.ObjectType):
    # Auth
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()  # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

    # Projects
    create_project = ProjectMutation.Field()

    # Shiritori
    create_game = CreateGameMutation.Field()
    start_game = StartGameMutation.Field()
    join_game = JoinGameMutation.Field()
    leave_game = LeaveGameMutation.Field()
    take_turn = TakeTurnMutation.Field()

    # Polls
    create_poll = CreatePollMutation.Field()
    vote_poll = PollVoteMutation.Field()
    clear_vote = ClearVoteMutation.Field()
