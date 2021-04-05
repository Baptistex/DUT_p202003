from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.mail) + str(timestamp)
        )
#account_activation_token = TokenGenerator()
account_activation_token = PasswordResetTokenGenerator()