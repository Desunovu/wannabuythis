class TestRedisActivationCodeStorage:
    USERNAME = "username"
    CODE = b"12345678"

    def test_get_activation_code(self, redis_client, redis_activation_code_storage):
        redis_client.set(self.USERNAME, self.CODE)
        assert (
            redis_activation_code_storage.get_activation_code(self.USERNAME) == self.CODE
        )

    def test_save_activation_code(self, redis_client, redis_activation_code_storage):
        redis_activation_code_storage.save_activation_code(self.USERNAME, self.CODE)
        assert redis_client.get(self.USERNAME) == self.CODE
