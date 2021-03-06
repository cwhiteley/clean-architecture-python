from unittest import mock, TestCase

from links.context import context
from links.repos.inmemory import MemoryBookmarkRepo, MemoryUserRepo
from links.usecases.interfaces import OutputBoundary, UseCase, View


class UseCaseTest(TestCase):

    def setUp(self):
        # ensure a new/clean instance of context repositories
        context.bookmark_repo = MemoryBookmarkRepo()
        context.user_repo = MemoryUserRepo()


class ControllerTestMixin:
    """
    Use this class to inherit common controller testing behavior.
    """

    def mixin_setup(self):
        self.usecase = mock.MagicMock()
        self.presenter = PresenterSpy()
        self.view = mock.Mock()
        self.request = {}

    def test_controller_passes_view_model_to_view(self):
        self.presenter.view_model = {'generic_view_model': True}
        self.controller.handle(self.request)
        self.view.generate_view.assert_called_with(self.presenter.view_model)


class PresenterSpy(OutputBoundary):

    def __init__(self):
        self.present_called = False
        self.present_errors_called = False

        self.response_model = None
        self.view_model = None

    def present(self, response_model):
        self.present_called = True
        self.response_model = response_model

    # def present_errors(self, response_model):
    #     self.present_errors_called = True
    #     self.response_model = response_model

    def get_view_model(self):
        return self.view_model


class UseCaseSpy(UseCase):

    presenter = None
    execute_was_called = False

    # def __init__(self, *args, **kwargs):
    #     pass

    def execute(self, presenter):
        self.presenter = presenter
        self.execute_was_called = True


class ViewSpy(View):

    view_model = None
    generate_view_was_called = False

    def generate_view(self, view_model):
        self.generate_view_was_called = True
        self.view_model = view_model


class ViewModelDouble:

    pass


