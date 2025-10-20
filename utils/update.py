import gzctf_api as api
import pprint
import sys
import os
import tomllib
import glob
import pyzipper
from io import BytesIO
from override import raise_for_status


def extract_category(dirname):
    assert dirname.split(os.path.sep)[-3] == "challenges", f"Invalid dirname {dirname}!"
    lowered_category = dirname.split(os.path.sep)[-2]
    return lowered_category[0].upper() + lowered_category[1:]


def config_merge(config, new_config, map_dict=None, optional=False):
    if not map_dict:
        return config.update(new_config)
    for target, key in map_dict.items():
        if key in new_config:
            config[target] = new_config[key]
        elif not optional:
            assert False, f"Key {key} not found in new_config"


def upload_attachment(challenge_id, file_name, data):
    asset = api.api_upload_asset(file_name, data)
    api.api_update_game_challenge_attachment(challenge_id, asset["hash"])
    print(f"上传附件到{challenge_id}: {asset['hash']}")


def set_attachment_url(challenge_id, remote_url):
    api.api_update_game_challenge_attachment(challenge_id, remote_url=remote_url)


@raise_for_status
def __main__():
    CHALLENGE = {}
    CHALLENGE_INFO = {}
    FLAGS = []

    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} (Chanllenges dir) (Container tag)")
        exit(0)

    root_dir = os.path.abspath(sys.argv[1])

    try:
        with open(os.path.join(root_dir, "challenge.toml"), "rb") as f:
            specification = tomllib.load(f)
            if "category" not in specification:
                specification["category"] = extract_category(root_dir)
    except Exception as e:
        print(f"加载题目配置失败: {e}")
        print(f"root_dir: {root_dir}")
        print(f"files: {os.listdir(root_dir)}")
        exit(1)

    has_container = "container" in specification
    is_static_container = has_container and specification["container"].get("static")
    is_dynamic_flag = has_container and not is_static_container

    config_merge(
        CHALLENGE,
        specification,
        {
            "title": "title",
            "category": "category",
        },
    )
    CHALLENGE["type"] = (
        "StaticAttachment"
        if not has_container
        else ("DynamicContainer" if is_dynamic_flag else "StaticContainer")
    )

    CHALLENGE_INFO["category"] = CHALLENGE["category"]
    CHALLENGE_INFO["content"] = "".join(
        [
            f"**Author:** {specification['author']} / "
            + f"**Difficulty:** {specification['difficulty']}\n\n---\n\n",
            (specification.get("description") or "").strip(),
        ]
    )
    if is_dynamic_flag:  # flag setup
        CHALLENGE_INFO["flagTemplate"] = specification["flag"]
    else:
        if isinstance(specification["flag"], str):  # TODO
            FLAGS = [specification["flag"]]
        else:
            FLAGS = specification["flag"]
    if specification.get("min_score_rate") and isinstance(
        specification["min_score_rate"], float
    ):
        CHALLENGE_INFO["minScoreRate"] = specification["min_score_rate"]
    CHALLENGE_INFO = api.DEFAULT_CHALLENGE_INFO | CHALLENGE_INFO

    if has_container:
        container = specification["container"]
        CHALLENGE_INFO = api.DEFAULT_CONTAINER_INFO | CHALLENGE_INFO
        config_merge(
            CHALLENGE_INFO,
            container,
            {
                "containerExposePort": "port",
                "memoryLimit": "memory",
                "storageLimit": "storage",
                "cpuCount": "cpu",
                "containerImage": "image",
            },
            optional=True,
        )
        if len(sys.argv) == 3:
            CHALLENGE_INFO["containerImage"] = sys.argv[-1] # type: ignore

    pprint.pprint(specification)
    pprint.pprint(CHALLENGE)
    pprint.pprint(CHALLENGE_INFO)

    assert CHALLENGE["category"] in api.ChallengeCategory

    challenges = api.api_get_game_challenges()

    is_exist = [
        *filter(
            lambda x: x["title"] == CHALLENGE["title"] and not x["isEnabled"],
            challenges,
        )
    ]

    if not is_exist:
        print(f"题目[{CHALLENGE['title']}]不存在，新建题目")
        challenge_id = api.api_add_game_challenge(CHALLENGE)["id"]
    else:
        challenge_id = is_exist[0]["id"]
    print(f"更新题目[{CHALLENGE['title']}] ID: {challenge_id}")
    api.api_update_game_challenge(challenge_id, CHALLENGE_INFO)

    # update attachment
    attachments_config = specification.get("attachments") or {}
    ATTACHMENTS_PATH = attachments_config.get("path") or "attachments/**"
    attachments_type = "list"
    attachments_name = attachments_config.get("name") or "attachments.zip"
    attachments_password = attachments_config.get("password")
    if isinstance(ATTACHMENTS_PATH, str):
        if ATTACHMENTS_PATH.endswith(".zip"):
            attachments_type = "zip"
        elif ATTACHMENTS_PATH.startswith("http"):
            attachments_type = "url"
        else:
            ATTACHMENTS_PATH = [ATTACHMENTS_PATH]

    if attachments_type == "list":
        real_attachments = []
        for path in ATTACHMENTS_PATH:
            real_attachments.extend(glob.glob(path, root_dir=root_dir, recursive=True))
        if real_attachments:
            attachment_zip = BytesIO()
            with pyzipper.AESZipFile(attachment_zip, "w") as z:
                if attachments_password:
                    z.setencryption(pyzipper.WZ_AES)
                    z.setpassword(attachments_password.encode())
                for attachment in real_attachments:
                    if os.path.isdir(attachment):
                        continue
                    z.write(
                        os.path.join(root_dir, attachment),
                        attachment,
                    )
            attachment_data = attachment_zip.getvalue()
            upload_attachment(challenge_id, attachments_name, attachment_data)
    elif attachments_type == "zip":
        with open(os.path.join(root_dir, ATTACHMENTS_PATH), "rb") as f: # type: ignore
            attachment_data = f.read()
        upload_attachment(challenge_id, attachments_name, attachment_data)
    elif attachments_type == "url":
        set_attachment_url(challenge_id, ATTACHMENTS_PATH)

    # upload flags
    if FLAGS:
        now_flags = api.api_get_game_challenge(challenge_id)["flags"]
        now_flags = [x["flag"] for x in now_flags]
        new_flags = set(FLAGS) - set(now_flags)
        if new_flags:
            api.api_update_game_challenge_flags(challenge_id, list(new_flags))
            print(f"添加静态 flag: {new_flags}")


if __name__ == "__main__":
    __main__()
