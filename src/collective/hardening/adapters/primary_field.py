from AccessControl.users import SpecialUser
from collective.hardening import _
from collective.hardening.controlpanel.settings import IHardeningSettings
from collective.hardening.interfaces import ICollectiveHardeningLayer
from fnmatch import fnmatch
from functools import cached_property
from logging import getLogger
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.formwidget.namedfile.validator import NamedFileWidgetValidator
from plone.memoize.view import memoize_contextless
from plone.namedfile.interfaces import INamedField
from plone.registry.interfaces import IRegistry
from plone.rfc822.interfaces import IPrimaryFieldInfo
from z3c.form import validator
from z3c.form.interfaces import NOT_CHANGED
from zExceptions import Forbidden
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import ValidationError


logger = getLogger(__name__)


class IValidateUpload(Interface):
    """Validate the uploaded file."""

    def validate():
        """Validate the primary field against the hardening settings."""


class DeniedExtensionValidationError(ValidationError):
    """Uploading files with this extension is not allowed."""


class DeniedMimetypeValidationError(ValidationError):
    """Uploading files with this mimetype is not allowed."""


class BaseUploadValidatorMixin:

    @property
    @memoize_contextless
    def settings(self):
        """The settings for the hardening."""
        registry = getUtility(IRegistry)
        return registry.forInterface(
            IHardeningSettings, prefix="collective.hardening.settings", check=False
        )


@implementer(IValidateUpload)
@adapter(IDexterityContent)
class ValidateUpload(BaseUploadValidatorMixin):
    def __init__(self, context):
        self.context = context

    @property
    @memoize_contextless
    def user_name(self):
        """Return the user name"""
        user = api.user.get_current()
        if isinstance(user, SpecialUser):
            # E.g. anonymous
            return user.name
        return api.user.get_current().getUserName()

    @cached_property
    def primary_field(self):
        primary_field_info = IPrimaryFieldInfo(self.context, None)
        return primary_field_info.value

    @cached_property
    def content_type(self):
        try:
            return self.primary_field.contentType
        except AttributeError:
            return None

    @cached_property
    def filename(self):
        try:
            return self.primary_field.filename
        except AttributeError:
            return None

    def raise_forbidden(self, message):
        api.portal.show_message(message, type="error")
        raise Forbidden(message)

    def validate_content_type(self):
        """Check if the mimetype is a valid one."""
        content_type = self.content_type
        if not content_type:
            return True

        deny_list = self.settings.mimetypes_deny_list
        if not deny_list:
            return True

        for mimetype in deny_list:
            if fnmatch(content_type, mimetype):
                logger.info(
                    "Preventing the upload of a file with the mimetype %r by %r.",
                    content_type,
                    self.user_name,
                )
                message = _(
                    "error_denied_mimetype",
                    default="Uploading files with the '${mimetype}' mimetype is not allowed.",
                    mapping={"mimetype": mimetype},
                )
                self.raise_forbidden(message)

        return True

    def validate_extension(self):
        """Check if the extension is a valid one."""
        filename = self.filename
        if not filename:
            return True

        deny_list = self.settings.extensions_deny_list
        if not deny_list:
            return True

        for extension in deny_list:
            if fnmatch(filename, f"*.{extension}"):
                logger.info(
                    "Preventing the upload of a file with the extension %r by %r.",
                    extension,
                    self.user_name,
                )
                message = _(
                    "error_denied_extension",
                    default="Uploading files with the '${extension}' extension is not allowed.",
                    mapping={"extension": extension.lower()},
                )
                self.raise_forbidden(message)

        return True

    def validate(self):
        """Validate the primary field against the hardening settings."""
        if not self.primary_field:
            return True
        return self.validate_content_type() and self.validate_extension()


class HardenedNamedFileWidgetValidator(
    NamedFileWidgetValidator, BaseUploadValidatorMixin
):

    def validate_content_type(self, value):
        """Check that the uploaded file content type is not in our deny list."""
        if value is None:
            return

        content_type = value.contentType
        if not content_type:
            return

        deny_list = self.settings.mimetypes_deny_list
        if not deny_list:
            return

        for mimetype in deny_list:
            if fnmatch(content_type, mimetype):
                message = _(
                    "error_denied_mimetype",
                    default="Uploading files with the '${mimetype}' mimetype is not allowed.",
                    mapping={"mimetype": mimetype},
                )
                raise DeniedMimetypeValidationError(message)

    def validate_extension(self, value):
        """Check that the uploaded file extension is not in our deny list."""
        if value is None:
            return

        filename = value.filename
        if not filename:
            return

        deny_list = self.settings.extensions_deny_list
        if not deny_list:
            return

        for extension in deny_list:
            if fnmatch(filename, f"*.{extension}"):
                message = _(
                    "error_denied_extension",
                    default="Uploading files with the '${extension}' extension is not allowed.",
                    mapping={"extension": extension.lower()},
                )
                raise DeniedExtensionValidationError(message)

    def validate(self, value, force=False):
        if value != NOT_CHANGED:
            self.validate_content_type(value)
            self.validate_extension(value)
        return super().validate(value, force=force)


validator.WidgetValidatorDiscriminators(
    HardenedNamedFileWidgetValidator,
    request=ICollectiveHardeningLayer,
    field=INamedField,
)
