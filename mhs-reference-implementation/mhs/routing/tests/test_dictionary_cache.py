import unittest
from unittest.mock import patch

import mhs.routing.dictionary_cache as dict_cache
from utilities.test_utilities import async_test
import time


class TestDictionaryCache(unittest.TestCase):

    @async_test
    async def test_get_empty_value(self):
        cache = dict_cache.DictionaryCache()
        value = await cache.retrieve_mhs_attributes_value("ods", "interaction")

        self.assertIsNone(value)

    @async_test
    async def test_get_basic_value(self):
        cache = dict_cache.DictionaryCache()
        self.assertTrue(not cache.cache)

        await cache.add_cache_value("code", "int", "check123")
        value = await cache.retrieve_mhs_attributes_value("code", "int")

        self.assertIsNotNone(value)
        self.assertEqual(value, "check123")

    @async_test
    async def test_cache_entry_not_expired(self):
        cache = dict_cache.DictionaryCache(1)  # Set timeout to 1s
        await cache.add_cache_value("code", "int", "check123")

        value = await cache.retrieve_mhs_attributes_value("code", "int")

        self.assertIsNotNone(value)
        self.assertEqual(value, "check123")

    @patch('time.time')
    @async_test
    async def test_message_should_timeout(self, patched_time):
        half_second = 0.5
        patched_time.return_value = 1

        cache = dict_cache.DictionaryCache(half_second)
        await cache.add_cache_value("code", "int", "check123")

        patched_time.return_value = 1.6

        value = await cache.retrieve_mhs_attributes_value("code", "int")

        self.assertIsNone(value)

    @patch('time.time')
    @async_test
    async def test_multiple_timeout(self, patched_time):
        cache = dict_cache.DictionaryCache(2)
        patched_time.return_value = 1
        await cache.add_cache_value("code", "int", "check123")

        patched_time.return_value = 2

        value = await cache.retrieve_mhs_attributes_value("code", "int")
        self.assertEqual(value, "check123")  # Check value in cache

        patched_time.return_value = 3.5  # value should expire in cache

        value = await cache.retrieve_mhs_attributes_value("code", "int")
        self.assertIsNone(value)

    @patch('time.time')
    @async_test
    async def test_ttl_does_not_change_on_read(self, patched_time):
        cache = dict_cache.DictionaryCache()
        patched_time.return_value = 1

        await cache.add_cache_value("code", "int", "check123")
        insert_time = cache.cache['code-int']['time']

        await cache.retrieve_mhs_attributes_value("code", "int")
        self.assertEqual(insert_time, cache.cache['code-int']['time'])

    @async_test
    async def test_invalid_timeout(self):
        with self.assertRaises(ValueError):
            dict_cache.DictionaryCache(-1)
