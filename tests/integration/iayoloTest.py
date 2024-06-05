import os
import sys
import numpy as np
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from unittest.mock import Mock, MagicMock, patch
from views.dashboardPageView import DashboardPage

class TestIAYOLO(unittest.TestCase):
    @patch('views.dashboardPageView.ImageTk')
    @patch('views.dashboardPageView.Image')
    @patch('views.dashboardPageView.S3Controller.uploadImage')
    @patch('views.dashboardPageView.DBController')
    @patch('views.dashboardPageView.DashboardPage.StartCamera.isValidLicensePlate')
    @patch('views.dashboardPageView.np')
    @patch('views.dashboardPageView.cv2')
    @patch('views.dashboardPageView.SocketController')
    @patch('views.dashboardPageView.socket.socket')
    @patch('views.dashboardPageView.AIController')
    @patch('views.dashboardPageView.PollController.currSetting', Mock())
    @patch('views.dashboardPageView.cont.loggedIn', True)
    @patch('views.dashboardPageView.cont.cameraEnabled', True)
    @patch('views.dashboardPageView.AIController.vehicle_detection_model.predictor', False)
    def test_ia_yolo_filter(self, mock_ai_controller, mock_socket, mock_socket_controller, mock_cv2, mock_np, mock_is_valid_license, mock_db_controller, mock_upload_image, mock_image, mock_image_tk):
        mock_cap = Mock()
        mock_cap.read.return_value = (True, np.array([[0] * 4 for _ in range(4)]))
        mock_ai_controller.setVehicleClasses = Mock()

        mock_box = Mock()
        mock_box.id = Mock(item=Mock(return_value=1))
        mock_box.cls = Mock(item=Mock(return_value=2))
        mock_box.xyxy = [[Mock(item=Mock(return_value=0))] * 4]
        mock_result = Mock()
        mock_result.boxes = [mock_box]
        mock_ai_controller.detect_vehicle.return_value = [mock_result]

        mock_lp_box = Mock()
        mock_lp_box.xyxy = [[Mock(item=Mock(return_value=0))] * 4]
        mock_lp_result = Mock()
        mock_lp_result.boxes = [mock_lp_box]
        mock_ai_controller.detect_license_plate.return_value = [mock_lp_result]

        mock_socket.return_value = Mock()
        mock_socket.connect = MagicMock()
        mock_socket_controller.sendImage = MagicMock()
        mock_socket.controller.receiveImage.return_value = [Mock(return_value=1)]
        mock_socket.close = MagicMock()

        mock_cv2.resize.return_value = [Mock(return_value=1)]
        mock_cv2.cvtColor.return_value = [Mock(return_value=2)]
        mock_cv2.GaussianBlur.return_value = [Mock(return_value=3)]
        mock_cv2.threshold.return_value = (Mock(), Mock(return_value=4))
        mock_np.ones.return_value = Mock(return_value=5)
        mock_cv2.dilate.return_value = Mock(return_value=6)
        mock_cv2.erode.return_value = Mock(return_value=7)

        mock_ai_controller.get_license_number_cnocr.return_value = [{'text': 'AAA111'}]
        mock_is_valid_license.return_value = True

        mock_db_controller.getCamera.return_value = Mock(location='morayta')
        mock_upload_image.return_value = 'url'
        mock_db_controller.addLicensePlate.return_value = Mock(ok=True)

        mock_image.fromarray.return_value = Mock(return_value=1)
        mock_image_tk.PhotoImage.return_value = Mock(return_value=2)

        start_camera = DashboardPage.StartCamera({'id': 0})
        start_camera.start(mock_cap, Mock(), 1, Mock(), Mock())
        self.assertEqual(start_camera.vehicleCount, 1)
        self.assertEqual(mock_ai_controller.setVehicleClasses.call_count, 4)

if __name__ == '__main__':
    unittest.main()