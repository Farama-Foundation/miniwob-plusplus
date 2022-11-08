from gymnasium.envs.registration import register


def register_miniwob_envs():
    register(
        id="miniwob/click-test-v0",
        entry_point="miniwob.environment:MiniWoBEnvironment",
        kwargs={"subdomain": "click-test"},
    )


register_miniwob_envs()
