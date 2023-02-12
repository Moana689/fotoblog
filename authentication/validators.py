from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError('Le mot de passe doit contenir une lettre', code='password_no_letters')
        if not any(char.islower() for char in password):
            raise ValidationError('Le mot de passe doit contenir un caractère minuscule', code='password_no_lower')
        if not any(char.isupper() for char in password):
            raise ValidationError('Le mot de passe doit contenir un caractère majuscule', code='password_no_upper')

    def get_help_text(self):
        return 'Le mot de passe doit contenir au moins une lettre majuscule et minuscule.'


class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError('Le mot de passe doit contenir un chiffre', code='password_no_digit')

    def get_help_text(self):
        return 'Le mot de passe doit contenir au moins un chiffre.'


# class ContainsSpecialCharValidator:
#     def validate(self, password, user=None):
#         if not any(char.)
