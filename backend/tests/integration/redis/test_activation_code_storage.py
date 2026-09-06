class TestRedisActivationCodeStorage:
    USERNAME = "username"
    CODE = "12345678"

    def test_save_and_get_activation_code(self, redis_activation_code_storage):
        redis_activation_code_storage.save_activation_code(self.USERNAME, self.CODE)
        assert (
            redis_activation_code_storage.get_activation_code(self.USERNAME)
            == self.CODE
        )
