import pytest
import os

from piptools.repositories import PyPIRepository
from piptools.scripts.compile import get_pip_command


@pytest.mark.parametrize(
    ('input', 'expected', 'prereleases'),

    ((tup + (False,))[:3] for tup in [

        # Make sure secondary reqs of top-level editable req are maintained
        # (['git+git://example.org/celery.git#egg=celery'],
        # (['-e tests/fixtures/fake_package'],
        (['{}'.format(os.path.join(os.path.dirname(__file__), 'fixtures', 'fake_package'))],
         []
         ),
    ])
)
def test_editable_resolver(base_resolver, repository, from_editable, input, expected, prereleases):
    input = [from_editable(line) for line in input]
    repository = get_repository()
    output = base_resolver(input, prereleases=prereleases, repository=repository).resolve()
    output = {str(line) for line in output}
    assert output == {str(line) for line in expected}


def get_repository():
    pip_command = get_pip_command()
    pip_args = []
    pip_options, _ = pip_command.parse_args(pip_args)
    session = pip_command._build_session(pip_options)
    repository = PyPIRepository(pip_options, session)
    return repository
