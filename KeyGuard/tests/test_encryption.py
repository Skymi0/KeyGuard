# -*- coding: utf-8 -*-
"""
    Secret Sharing Unit Tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains unit tests for verifying the functionality of the Shamir 
    Secret Sharing implementation. It uses the unittest framework for test 
    organization and execution.

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import random
import unittest
from keyshard import SecretSharer

class EncryptionTest(unittest.TestCase):
    def setUp(self):
        """Set up the environment for each test."""
        pass  # Implement any necessary setup for your tests here

    def tearDown(self):
        """Clean up after each test."""
        pass  # Implement any necessary cleanup for your tests here

    def split_and_recover_secret(self, sharer_class, m, n, secret):
        """
        Split a secret into shares and then recover it from a subset of those shares.

        Args:
            sharer_class: The class implementing the secret sharing scheme.
            m (int): The minimum number of shares required to recover the secret.
            n (int): The total number of shares created.
            secret (str): The secret to be shared.
        
        Raises:
            AssertionError: If the recovered secret does not match the original secret.
        """
        # Split the secret into shares
        shares = sharer_class.split_secret(secret, m, n)
        random.shuffle(shares)  # Shuffle shares to simulate distribution
        
        # Recover the secret from the first m shares
        recovered_secret = sharer_class.recover_secret(shares[0:m])
        
        # Assert that the recovered secret matches the original secret
        assert(recovered_secret == secret)


    def test_hex_to_hex_sharing(self):
        """Test case for hex to hex sharing."""
        recovered_secret = self.split_and_recover_secret(
            sharer_class=SecretSharer(), 
            m=3,
            n=5,
            secret="c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a"
        )
