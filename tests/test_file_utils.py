import pytest

import cpplibhub.file_utils as files


@pytest.fixture(scope="session")
def existing_dir(tmpdir_factory):
    ed = tmpdir_factory.mktemp("existing_dir")
    print("\n*** Created temporary dir for current session: ", ed)
    return ed


@pytest.fixture(scope="session")
def existing_text_file(existing_dir):
    ef = existing_dir.join("existing_file.txt")
    result = files.write_text_file_noexcept(ef, "test")
    assert not result["error"]
    print("\n*** Created temporary text file for current session: ", ef)
    return ef


@pytest.fixture(scope="session")
def existing_text_file_symlink(existing_dir, existing_text_file):
    es = existing_dir + "/existing_text_file_symlink.txt"
    assert not files.create_symlink_noexcept(existing_text_file, es)["error"]
    print("\n*** Created temporary symlink for current session: ", es)
    return es


@pytest.fixture(scope="session")
def not_existing_dir():
    return "/tmp/this_dir_does_not_exist"


@pytest.fixture(scope="session")
def not_existing_file():
    return "/tmp/this_file_does_not_exist"


def test_file_exists(existing_text_file, not_existing_file):
    assert files.file_exists(existing_text_file)
    assert not files.file_exists(not_existing_file)


def test_dir_exists(existing_dir, not_existing_dir):
    assert files.dir_exists(existing_dir)
    assert not files.dir_exists(not_existing_dir)


def test_symlink_exists(existing_text_file_symlink):
    assert files.symlink_exists(existing_text_file_symlink)


def test_create_remove_symlink_noexcept(existing_text_file, existing_dir):
    # Create and remove symlink to file
    text_file_symlink = existing_dir + "/file_symlink.txt"
    assert not files.create_symlink_noexcept(existing_text_file, text_file_symlink)["error"]
    assert files.symlink_exists(text_file_symlink)
    assert files.remove_symlink_noexcept(text_file_symlink)
    assert not files.symlink_exists(text_file_symlink)

    # Create and remove symlink to dir
    dir_symlink = existing_dir + "/symlink_to_parent_dir"
    assert files.create_symlink_noexcept(existing_dir, dir_symlink)
    assert files.symlink_exists(dir_symlink)
    assert files.remove_symlink_noexcept(dir_symlink)
    assert not files.symlink_exists(dir_symlink)


def test_path_base_and_leaf():
    path = "/tmp/base/leaf"
    base, leaf = files.path_base_and_leaf(path)
    assert base == "/tmp/base"
    assert leaf == "leaf"
    # Test with forward slash at the end
    path = "/tmp/base/leaf/"
    base, leaf = files.path_base_and_leaf(path)
    assert base == "/tmp/base"
    assert leaf == "leaf"


def test_read_write_text_file_noexcept(existing_dir):
    tmpfile = existing_dir + "/tmpfile.txt"
    assert not files.write_text_file_noexcept(tmpfile, "test")["error"]
    read_result = files.read_text_file_noexcept(tmpfile)
    assert not read_result["error"]
    assert read_result["contents"] == "test"
    files.remove_file_noexcept(tmpfile)


def test_create_path_noexcept(existing_dir):
    path = existing_dir + "/some/complicated/path"
    assert not files.create_path_noexcept(path)["error"]
    assert not files.remove_dir_noexcept(existing_dir + "/some")["error"]


def test_copy_file_noexcept(existing_dir, existing_text_file):
    dest = existing_dir + "/existing_text_file_copy.txt"
    assert not files.copy_file_noexcept(existing_text_file, dest)["error"]
    # Read created copy to verify its contents
    assert "test" == files.read_text_file_noexcept(dest)["contents"]
    # Remove created copy
    assert not files.remove_file_noexcept(dest)["error"]


def test_move_file_noexcept(existing_dir):
    # Create temp file
    orig_file = existing_dir + "move_file_test.txt"
    dest = existing_dir + "moved_file.txt"
    contents = "move_file_test.txt"
    assert not files.write_text_file_noexcept(orig_file,
                                              contents)["error"]
    # Move it
    assert not files.move_file_noexcept(orig_file, dest)["error"]
    # Assert original file not exists
    assert not files.file_exists(orig_file)
    # Assert moved file exists and has correct contents
    assert files.file_exists(dest)
    assert contents == files.read_text_file_noexcept(dest)["contents"]
    # Remove temp file
    assert files.remove_file_noexcept(dest)


def test_copy_dir_noexcept(existing_dir):
    # Create path
    orig_path = existing_dir + "/copy/dir/test"
    assert not files.create_path_noexcept(orig_path)["error"]
    src = existing_dir + "/copy"
    dest = existing_dir + "/dest"
    # Copy tree
    assert not files.copy_dir_noexcept(src, dest)["error"]
    # Assert both exist
    assert files.dir_exists(orig_path)
    assert files.dir_exists(dest + "/dir/test")
    # Remove src and dest
    assert not files.remove_dir_noexcept(src)["error"]
    assert not files.remove_dir_noexcept(dest)["error"]


def test_move_dir_noexcept(existing_dir):
    # Create path
    orig_path = existing_dir + "/move/dir/test"
    assert not files.create_path_noexcept(orig_path)["error"]
    src = existing_dir + "/move"
    dest = existing_dir + "/dest"
    # Copy tree
    assert not files.move_dir_noexcept(src, dest)["error"]
    # Assert only dest exists
    assert not files.dir_exists(orig_path)
    assert files.dir_exists(dest + "/dir/test")
    # Remove dest
    assert not files.remove_dir_noexcept(dest)["error"]


def test_get_subdirs(existing_dir):
    # Create path
    path1 = existing_dir + "/subdirs/test1/test1_1"
    assert not files.create_path_noexcept(path1)["error"]
    path2 = existing_dir + "/subdirs/test2/test1_2"
    assert not files.create_path_noexcept(path2)["error"]
    subdirs_result = files.get_subdirs(existing_dir + "/subdirs")
    # There must be no error when getting subdirs
    assert not subdirs_result['error']
    subdirs = subdirs_result["subdirs"]
    # There must be 2 subdirs, check their names
    assert len(subdirs) == 2
    assert "test1" in subdirs
    assert "test2" in subdirs
    # Cleanup
    assert not files.remove_dir_noexcept(existing_dir + "/subdirs")["error"]


def test_get_file_list(existing_dir):
    # Create path
    path = existing_dir + "/file_list_test"
    assert not files.create_path_noexcept(path)["error"]
    # Create a file, a dir and a symlink in that dir
    files.create_path_noexcept(path + "/test_dir")
    files.write_text_file_noexcept(path + "/test_file.txt", "test_file.txt")
    files.create_symlink_noexcept(path + "/test_file.txt", path + "/test_file_symlink.txt")
    # Assert that only file is recognized as file
    result = files.get_file_list(path)
    assert not result["error"]
    assert len(result["file_list"]) == 2
    assert "test_file.txt" in result["file_list"]
    assert "test_file_symlink.txt" in result["file_list"]

    # Cleanup
    files.remove_dir_noexcept(path)


def test_get_total_items(existing_dir):
    """
    Tests:
    get_total_items,
    dir_empty,
    get_item_type
    """
    # Create path
    path = existing_dir + "/get_total_items_test"
    assert not files.create_path_noexcept(path)["error"]
    # Create a file, a dir and a symlink in that dir
    files.create_path_noexcept(path + "/test_dir")
    files.write_text_file_noexcept(path + "/test_file.txt", "test_file.txt")
    files.create_symlink_noexcept(path + "/test_file.txt", path + "/test_file_symlink.txt")
    # Assert there are 3 items
    result = files.get_total_items(path)
    assert not result["error"]
    assert result["total_items"] == 3
    # test_dir_empty test
    assert not files.dir_empty(path)
    assert files.dir_empty(path + "/not_exists")
    assert files.dir_empty(path + "/test_dir")
    # get_item_type test
    assert files.get_item_type(path)["item_type"] == "dir"
    assert files.get_item_type(path + "/test_file.txt")["item_type"] == "file"
    assert files.get_item_type(path + "/test_file_symlink.txt")["item_type"] == "symlink"
    assert not files.get_item_type(path + "/not_exists")["item_type"]
    # Cleanup
    files.remove_dir_noexcept(path)


def test_env_variables():
    """
    set_env_var,
    get_env_var,
    unset_env_var,
    env_var_exists
    """
    env_var = "dummy_env_var"
    assert not files.env_var_exists(env_var)
    files.set_env_var(env_var, "exists")
    assert files.env_var_exists(env_var)
    assert files.get_env_var(env_var) == "exists"
    files.unset_env_var(env_var)
    assert not files.env_var_exists(env_var)


def test_tar_gz(existing_dir):
    """
    unzip_tar_gz,
    zip_file_tar_gz,
    zip_dir_tar_gz
    """

    # Create a directory with text file
    path = existing_dir + "/tar_gz_test"
    assert not files.create_path_noexcept(path)["error"]
    # Create a dir and a file
    src_dir = path + "/test_dir"
    files.create_path_noexcept(src_dir + "/inner_dir")
    src_file = src_dir + "/test_file.txt"
    src_file_contents = "test_file.txt"
    files.write_text_file_noexcept(src_file, src_file_contents)

    # Create .tar.gz archive from file
    assert not files.zip_file_tar_gz(src_file, path + "/result_file.tar.gz")["error"]

    # Create .tar.gz archive from directory
    assert not files.zip_dir_tar_gz(src_dir, path + "/result_dir.tar.gz")["error"]

    # Unzip .tar.gz and verify contents
    assert not files.unzip_tar_gz(path + "/result_file.tar.gz",
                                  path + "/unzipped")["error"]
    assert files.file_exists(path + "/unzipped/test_file.txt")
    assert files.read_text_file_noexcept(path +
                                         "/unzipped/test_file.txt")["contents"] == src_file_contents

    # Unzip .tar.gz dir and verify contents
    assert not files.unzip_tar_gz(path + "/result_dir.tar.gz",
                                  path + "/unzipped")["error"]
    assert files.dir_exists(path + "/unzipped/test_dir")
    assert files.file_exists(path + "/unzipped/test_dir/test_file.txt")
    assert files.read_text_file_noexcept(path +
                                         "/unzipped/test_dir/test_file.txt")["contents"] \
        == src_file_contents

    # Cleanup
    assert not files.remove_dir_noexcept(existing_dir + "/tar_gz_test")["error"]


def test_download_into_file(existing_dir):
    dest_file = existing_dir + '/tmp.md'
    assert not files.download_into_file("https://github.com/iotanbo/cpplibhub/blob/master/docs/GET_STARTED.md",
                                        dest_file)['error']
    # Cleanup
    files.remove_file_noexcept(dest_file)
