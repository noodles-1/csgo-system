import os
import sys
import unittest
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from unittest.mock import patch, MagicMock
from controllers.s3controller import S3Controller

class TestS3ControllerMethods(unittest.TestCase):
    @patch('controllers.s3controller.boto3.client')
    def test_upload_image(self, mock_s3_client):
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = None
        mock_s3_client.return_value = mock_s3

        s3 = S3Controller()
        
        image = np.zeros((1, 1, 1), dtype=np.uint8)
        image_name = 'test_image'

        result = s3.uploadImage(image, image_name)
        mock_s3.put_object.assert_called_once()

        _, kwargs = mock_s3.put_object.call_args
        self.assertIn('Bucket', kwargs)
        self.assertIn('Key', kwargs)
        self.assertIn('Body', kwargs)
        self.assertEqual(kwargs['ContentType'], 'image/jpeg')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()