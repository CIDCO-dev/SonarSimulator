import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import Mock, call, patch

from sonar_simulator import (
    checksum,
    generate_nmea_dbt,
    generate_nmea_dpt,
    generate_nmea_sentence,
    main,
)


class TestNMEAGenerator(unittest.TestCase):
    @staticmethod
    def _fake_now(second):
        return datetime(2026, 1, 1, 0, 0, second)

    def test_generate_nmea_dpt(self):
        depth = 15.5
        expected_output = "$SDDPT,15.5,0.1,100*7A"
        self.assertEqual(generate_nmea_dpt(depth), expected_output)

    def test_generate_nmea_dbt(self):
        depth = 15.5
        expected_output = "$SDDBT,50.9,f,15.5,M,8.5,F*06"
        self.assertEqual(generate_nmea_dbt(depth), expected_output)

    def test_generate_nmea_sentence_invalid_type(self):
        with self.assertRaises(ValueError):
            generate_nmea_sentence(10.0, "xyz")

    def test_checksum(self):
        sentence = "SDDPT,15.5,0.1,100"
        expected_checksum = "$SDDPT,15.5,0.1,100*7A"
        self.assertEqual(checksum(sentence), expected_checksum)

    @patch("sonar_simulator.serial.Serial")
    def test_main_writes_expected_dpt_frames(self, mock_serial):
        mock_ser = Mock()
        mock_ser.is_open = True
        mock_serial.return_value = mock_ser

        now_values = [
            self._fake_now(0),
            self._fake_now(1),
            self._fake_now(2),
        ]
        now_iter = iter(now_values)
        sleep_mock = Mock()

        output = StringIO()
        with patch("sys.stdout", output):
            main(
                "test_port_serie",
                9600,
                iterations=3,
                now_provider=lambda: next(now_iter),
                sleep_func=sleep_mock,
            )

        mock_serial.assert_called_once_with("test_port_serie", 9600, timeout=1)

        expected_nmea_sentences = [
            b"$SDDPT,10.0,0.1,100*7A\r\n",
            b"$SDDPT,11.0,0.1,100*7B\r\n",
            b"$SDDPT,12.0,0.1,100*78\r\n",
        ]
        self.assertEqual(
            mock_ser.write.call_args_list,
            [call(sentence) for sentence in expected_nmea_sentences],
        )
        self.assertIn("Connected to serial port test_port_serie at 9600 baud.", output.getvalue())
        self.assertEqual(sleep_mock.call_count, 2)
        mock_ser.close.assert_called_once()

    @patch("sonar_simulator.serial.Serial")
    def test_main_writes_expected_dbt_frames(self, mock_serial):
        mock_ser = Mock()
        mock_ser.is_open = True
        mock_serial.return_value = mock_ser

        now_values = [
            self._fake_now(0),
            self._fake_now(1),
            self._fake_now(2),
        ]
        now_iter = iter(now_values)
        sleep_mock = Mock()

        output = StringIO()
        with patch("sys.stdout", output):
            main(
                "test_port_serie",
                9600,
                sentence_type="dbt",
                iterations=3,
                now_provider=lambda: next(now_iter),
                sleep_func=sleep_mock,
            )

        mock_serial.assert_called_once_with("test_port_serie", 9600, timeout=1)

        expected_nmea_sentences = [
            b"$SDDBT,32.8,f,10.0,M,5.5,F*0E\r\n",
            b"$SDDBT,36.1,f,11.0,M,6.0,F*04\r\n",
            b"$SDDBT,39.4,f,12.0,M,6.6,F*0B\r\n",
        ]
        self.assertEqual(
            mock_ser.write.call_args_list,
            [call(sentence) for sentence in expected_nmea_sentences],
        )
        self.assertEqual(sleep_mock.call_count, 2)
        mock_ser.close.assert_called_once()

    @patch("sonar_simulator.serial.Serial", side_effect=RuntimeError("boom"))
    def test_main_handles_serial_open_errors(self, mock_serial):
        output = StringIO()
        with patch("sys.stdout", output):
            main("bad_port", 9600, iterations=1)
        mock_serial.assert_called_once_with("bad_port", 9600, timeout=1)
        self.assertIn("An error occurred: boom", output.getvalue())


if __name__ == "__main__":
    unittest.main()
