from analysis.Analysis import Analysis

#create an Analysis instance
analysis_instance = Analysis('configs/analysis_config.yml')

# load the marvel data
analysis_instance.load_data()

# retrive characters with stories number
analysis_instance.compute_analysis()

# data plot
analysis_instance.plot_data()