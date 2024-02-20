from analysis.Analysis import Analysis

import logging

def test_load_data():
    analysis = Analysis('configs/analysis_config.yml')  # Provide a test configuration file
    analysis.load_data()
    assert analysis.raw_data is not None

def test_compute_analysis():
    analysis = Analysis('configs/analysis_config.yml')  # Provide a test configuration file
    analysis.load_data()
    analysis_output = analysis.compute_analysis()
    assert analysis_output is not None

def test_notify_done():
    analysis = Analysis('configs/analysis_config.yml')  # Provide a test configuration file
    assert analysis.notify_done("Test notification") is None

def test_plot_data():
    analysis = Analysis('configs/analysis_config.yml')  # Provide a test configuration file
    analysis.load_data()
    fig = analysis.plot_data()
    assert fig is not None
