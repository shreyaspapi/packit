from pathlib import Path
from tests.conftest import mock_spec_download_remote_s
from tests.utils import get_specfile
from packit.utils import cwd
    spec = get_specfile(str(distgit / "beer.spec"))
def test_basic_local_update_empty_patch(
    spec = get_specfile(str(distgit / "beer.spec"))
    spec_package_section = ""
    for section in spec.spec_content.sections:
        if "%package" in section[0]:
            spec_package_section += "\n".join(section[1])
    assert "# PATCHES FROM SOURCE GIT" not in spec_package_section
    assert not spec.patches["applied"]
    assert not spec.patches["not_applied"]
    spec = get_specfile(str(distgit / "beer.spec"))
    spec_package_section = ""
    for section in spec.spec_content.sections:
        if "%package" in section[0]:
            spec_package_section += "\n".join(section[1])
    assert "Patch0002: 0002" not in spec_package_section  # no empty patches



def test_srpm(mock_remote_functionality_sourcegit, api_instance_source_git):
    # TODO: we need a better test case here which will mimic the systemd use case
    sg_path = Path(api_instance_source_git.upstream_local_project.working_dir)
    mock_spec_download_remote_s(sg_path / "fedora")
    with cwd(sg_path):
        api_instance_source_git.create_srpm(upstream_ref="0.1.0")
    assert list(sg_path.glob("beer-0.1.0-1.*.src.rpm"))[0].is_file()