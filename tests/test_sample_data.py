"""Tests for the sample data module."""
from unittest.mock import MagicMock, patch

import pytest

from brillouin_imaging._sample_data import (
    load_sample_data,
    sample_data_drosophila,
    sample_data_zfeye,
    sample_data_zfSBS,
    sample_data_beadsFTBM,
)


class TestSampleDataFunctions:
    """Tests for individual sample data functions."""

    @patch('brillouin_imaging._sample_data.load_sample_data')
    def test_sample_data_drosophila(self, mock_load):
        """Test sample_data_drosophila uses the BioImage archive URL."""
        sample_data_drosophila()

        mock_load.assert_called_once_with(
            'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/drosophila_LSBM.brim.zarr'
        )

    @patch('brillouin_imaging._sample_data.load_sample_data')
    def test_sample_data_zfeye(self, mock_load):
        """Test sample_data_zfeye uses the BioImage archive URL."""
        sample_data_zfeye()

        mock_load.assert_called_once_with(
            'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/zebrafish_eye_confocal.brim.zarr'
        )

    @patch('brillouin_imaging._sample_data.load_sample_data')
    def test_sample_data_zfSBS(self, mock_load):
        """Test sample_data_zfSBS uses the BioImage archive URL."""
        sample_data_zfSBS()

        mock_load.assert_called_once_with(
            'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/zebrafish_ECM_SBS.brim.zarr'
        )

    @patch('brillouin_imaging._sample_data.load_sample_data')
    def test_sample_data_beadsFTBM(self, mock_load):
        """Test sample_data_beadsFTBM uses the BioImage archive URL."""
        sample_data_beadsFTBM()

        mock_load.assert_called_once_with(
            'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/oil_beads_FTBM.brim.zarr'
        )


class TestLoadSampleDataPlaceholderRemoval:
    """Tests for the placeholder points layer scheduled removal in load_sample_data."""

    @pytest.mark.qt
    @patch('brillouin_imaging._sample_data.reader_function')
    @patch('brillouin_imaging._sample_data.napari.current_viewer')
    def test_placeholder_layer_is_removed_after_event_loop_iteration(
        self, mock_current_viewer, mock_reader_function, qtbot
    ):
        """The placeholder layer is returned immediately, then removed once the scheduled callback runs."""
        mock_layer = MagicMock()
        mock_viewer = MagicMock()
        mock_viewer.layers.__getitem__.return_value = mock_layer
        mock_current_viewer.return_value = mock_viewer

        result = load_sample_data('https://example.com/data.brim.zarr')

        mock_reader_function.assert_called_once_with('https://example.com/data.brim.zarr')
        data, add_kwargs, layer_type = result[0]
        assert add_kwargs == {
            "name": "_brillouin_sampledata_placeholder",
            "visible": False,
        }
        assert layer_type == "points"
        # the removal is scheduled, not immediate
        mock_viewer.layers.remove.assert_not_called()

        # let QTimer.singleShot(0, ...) fire on the real Qt event loop
        qtbot.waitUntil(lambda: mock_viewer.layers.remove.called, timeout=2000)

        mock_viewer.layers.__getitem__.assert_called_with(
            "_brillouin_sampledata_placeholder"
        )
        mock_viewer.layers.remove.assert_called_once_with(mock_layer)

    @pytest.mark.qt
    @patch('brillouin_imaging._sample_data.reader_function')
    @patch('brillouin_imaging._sample_data.napari.current_viewer')
    def test_placeholder_removal_is_a_noop_if_layer_already_gone(
        self, mock_current_viewer, mock_reader_function, qtbot
    ):
        """If the placeholder layer was already removed, the scheduled callback should not raise or remove anything else."""
        mock_viewer = MagicMock()
        mock_viewer.layers.__getitem__.side_effect = KeyError(
            "_brillouin_sampledata_placeholder"
        )
        mock_current_viewer.return_value = mock_viewer

        load_sample_data('https://example.com/data.brim.zarr')

        # give the event loop a chance to run the scheduled callback
        qtbot.wait(200)

        mock_viewer.layers.remove.assert_not_called()