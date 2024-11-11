import base64
import string
import secrets
import hashlib
import os
from six import integer_types
from cryptography.fernet import Fernet
from utilitybelt import int_to_charset, charset_to_int
from keyshard.primes import get_large_enough_prime
from keyshard.polynomials import random_polynomial, get_polynomial_points, modular_lagrange_interpolation

# Default character set for key generation
DEFAULT_CHAR_SET = string.ascii_letters + string.digits + string.punctuation

def secret_int_to_points(secret_int, point_threshold, num_points, prime=None):
    """
    Split a secret (integer) into shares (pair of integers / x,y coordinates).
    
    Samples the points of a random polynomial with the y-intercept equal to
    the secret integer.
    """
    if point_threshold < 2:
        raise ValueError("Threshold must be >= 2.")
    if point_threshold > num_points:
        raise ValueError("Threshold must be < the total number of points.")
    if prime is None:
        prime = get_large_enough_prime([secret_int, num_points])
    if prime is None:
        raise ValueError("Error! Secret is too long for share calculation!")

    coefficients = random_polynomial(point_threshold - 1, secret_int, prime)
    points = get_polynomial_points(coefficients, num_points, prime)
    return points

def point_to_share_string(point, charset):
    """
    Convert a point (a tuple of two integers) into a share string - that is,
    a representation of the point that uses the charset provided.
    """
    if '-' in charset:
        raise ValueError('The character "-" cannot be in the supplied charset.')
    if not (isinstance(point, tuple) and len(point) == 2 and
            isinstance(point[0], integer_types) and
            isinstance(point[1], integer_types)):
        raise ValueError('Point format is invalid. Must be a pair of integers.')

    x, y = point
    x_string = int_to_charset(x, charset)
    y_string = int_to_charset(y, charset)
    share_string = f"{x_string}-{y_string}"
    return share_string

def share_string_to_point(share_string, charset):
    """
    Convert a share string to a point (a tuple of integers).
    """
    if '-' in charset:
        raise ValueError('The character "-" cannot be in the supplied charset.')
    if not isinstance(share_string, str) or share_string.count('-') != 1:
        raise ValueError('Share format is invalid.')

    x_string, y_string = share_string.split('-')
    if (set(x_string) - set(charset)) or (set(y_string) - set(charset)):
        raise ValueError("Share has characters that aren't in the charset.")
    
    x = charset_to_int(x_string, charset)
    y = charset_to_int(y_string, charset)
    return (x, y)

def points_to_secret_int(points, prime=None):
    """
    Join integer points into a secret integer.

    Get the intercept of a random polynomial defined by the given points.
    """
    if not isinstance(points, list):
        raise ValueError("Points must be in list form.")
    for point in points:
        if not isinstance(point, tuple) or len(point) != 2:
            raise ValueError("Each point must be a tuple of two values.")
        if not (isinstance(point[0], integer_types) and
                isinstance(point[1], integer_types)):
            raise ValueError("Each value in the point must be an int.")
    
    x_values, y_values = zip(*points)
    if prime is None:
        prime = get_large_enough_prime(y_values)
    
    free_coefficient = modular_lagrange_interpolation(0, points, prime)
    return free_coefficient  # The secret integer is the free coefficient
def string_to_hex(input_string):
    try:
        if isinstance(input_string, bytes):
            byte_representation = input_string
        elif isinstance(input_string, str):
            byte_representation = input_string.encode('utf-8')
        else:
            raise ValueError("Input must be a string or bytes.")

        hex_representation = byte_representation.hex()
        return hex_representation
    except Exception as e:
        print(f"Error: {e}")

class SecretSharer:
    """ 
    Creates a secret sharer, which can convert from a secret string to a
    list of shares and vice versa. The splitter is initialized with the
    character set of the secrets and the character set of the shares that
    it expects to be dealing with.
    """
    
    secret_charset = string.hexdigits[:16]
    share_charset = string.hexdigits[:16]
    default_char_set = string.ascii_letters + string.digits + string.punctuation
    def __init__(self):
        pass
    
    def split_secret(self, secret_string, share_threshold, num_shares):
        """
        Split the secret string into shares.
        """
        secret_int = charset_to_int(string_to_hex(secret_string), self.secret_charset)
        points = secret_int_to_points(secret_int, share_threshold, num_shares)
        shares = [point_to_share_string(point, self.share_charset) for point in points]
        return shares

    def recover_secret(self, shares):
        """
        Recover the secret string from shares.
        """
        points = [share_string_to_point(share, self.share_charset) for share in shares]
        secret_int = points_to_secret_int(points)
        secret_string = int_to_charset(secret_int, self.secret_charset)
        return secret_string
