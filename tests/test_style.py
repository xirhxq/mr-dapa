import pytest
import matplotlib
matplotlib.use('agg')

from mr_dapa import StyleConfig, get_style, get_palette
from mr_dapa.drawers.base import BaseDrawer


class TestStyleConfig:

    def test_default_values(self):
        cfg = StyleConfig()
        assert cfg.dpi == 300
        assert cfg.figsize == (16, 9)
        assert cfg.format == 'png'
        assert cfg.background == 'white'

    def test_custom_values(self):
        cfg = StyleConfig(dpi=600, figsize=(10, 8), format='svg')
        assert cfg.dpi == 600
        assert cfg.figsize == (10, 8)
        assert cfg.format == 'svg'


class TestPresets:

    def test_paper_preset(self):
        cfg = get_style('paper')
        assert cfg.figsize == (8, 6)
        assert cfg.dpi == 300
        assert cfg.title_size == 16

    def test_presentation_preset(self):
        cfg = get_style('presentation')
        assert cfg.figsize == (16, 9)
        assert cfg.dpi == 150
        assert cfg.line_width == 2.5

    def test_dark_preset(self):
        cfg = get_style('dark')
        assert cfg.background == '#1a1a2e'
        assert cfg.line_width == 2.0

    def test_unknown_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown style"):
            get_style('nonexistent')

    def test_preset_returns_new_instance(self):
        a = get_style('paper')
        b = get_style('paper')
        a.dpi = 999
        assert b.dpi == 300


class TestPalettes:

    def test_default_palette(self):
        pal = get_palette('default')
        assert len(pal) == 10
        assert all(isinstance(c, str) for c in pal)

    def test_colorblind_palette(self):
        pal = get_palette('colorblind')
        assert len(pal) >= 8

    def test_vivid_palette(self):
        pal = get_palette('vivid')
        assert len(pal) >= 8

    def test_muted_palette(self):
        pal = get_palette('muted')
        assert len(pal) >= 8

    def test_unknown_palette_raises(self):
        with pytest.raises(ValueError, match="Unknown palette"):
            get_palette('nonexistent')

    def test_palette_returns_copy(self):
        a = get_palette('default')
        b = get_palette('default')
        a.append('#000000')
        assert len(b) == 10


class TestDrawerStyleAPI:

    def test_set_style_chain(self, tmp_path, sample_data, components_config):
        import json
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(sample_data))

        drawer = BaseDrawer(files=[str(data_file)], components=components_config)
        result = drawer.set_style('paper')
        assert result is drawer
        assert drawer.style.figsize == (8, 6)

    def test_set_palette_chain(self, tmp_path, sample_data, components_config):
        import json
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(sample_data))

        drawer = BaseDrawer(files=[str(data_file)], components=components_config)
        result = drawer.set_palette('colorblind')
        assert result is drawer
        assert len(drawer.style.palette) >= 8

    def test_combined_chain(self, tmp_path, sample_data, components_config):
        import json
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(sample_data))

        drawer = BaseDrawer(files=[str(data_file)], components=components_config)
        drawer.set_style('paper').set_palette('vivid')
        assert drawer.style.figsize == (8, 6)
        assert drawer.style.palette == get_palette('vivid')

    def test_svg_export(self, tmp_path, sample_data, components_config):
        import json
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(sample_data))

        from mr_dapa import StaticGlobalPlotDrawer
        drawer = StaticGlobalPlotDrawer(files=[str(data_file)], components=components_config)
        drawer.style.format = 'svg'
        fig = drawer.draw(['x'], save=True)
        assert fig is not None

        svg_files = list(tmp_path.glob('**/*.svg'))
        assert len(svg_files) == 1

    def test_pdf_export(self, tmp_path, sample_data, components_config):
        import json
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(sample_data))

        from mr_dapa import StaticGlobalPlotDrawer
        drawer = StaticGlobalPlotDrawer(files=[str(data_file)], components=components_config)
        drawer.style.format = 'pdf'
        fig = drawer.draw(['x'], save=True)
        assert fig is not None

        pdf_files = list(tmp_path.glob('**/*.pdf'))
        assert len(pdf_files) == 1
