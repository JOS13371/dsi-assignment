from typing import Any, Optional
import matplotlib.pyplot as plt
import requests
import json
import logging
import yaml

class Analysis:
    
    def __init__(self, analysis_config: str):
        # Initialize logger
        logging.basicConfig(level=logging.DEBUG)  # You can configure logging as per your requirements

        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']
        paths = CONFIG_PATHS + [analysis_config]
        config = {}

        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            
            if this_config:
                config.update(this_config)

        self.config = config
        self.raw_data = None
        self.repo_name = []
        self.repo_stars = []
        

    def load_data(self) -> None:
        try:
            marvel_response = requests.get(self.config['url'], params={"ts": self.config['ts'], "apikey": self.config['apikey'], "hash": self.config['hash']})
            marvel_response.raise_for_status()  # Raise an exception for HTTP errors
            self.raw_data = marvel_response.text
        except requests.exceptions.RequestException as e:
            logging.warning(f'Unable to retrieve Information from Marvel: {e}')
            self.raw_data = None  # Set raw_data to None upon failure
        

    def compute_analysis(self) -> None:
        if not self.raw_data:
            logging.error('No data available for analysis')
            return None  # Return None if no data is available
        
        json_data = json.loads(self.raw_data)
        items = json_data['data']['results']

        for item in items:
            self.repo_name.append(item['name'])
            self.repo_stars.append(item['stories']['available'])
        
        return True  # Example: Return a meaningful output indicating success


    def plot_data(self, save_path: Optional[str] = None, show_plot: bool = True) -> plt.Figure:
        if not self.repo_name or not self.repo_stars:
            logging.error('No data available for plotting')
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, 'No data available for plotting', horizontalalignment='center', verticalalignment='center')
            ax.set_axis_off()  # Hide axes
            return fig

        fig, ax = plt.subplots()
        ax.barh(self.repo_name, self.repo_stars)
        ax.set_xlabel(self.config['xlabel'])
        ax.set_ylabel(self.config['ylabel'])
        ax.set_title(self.config['title'])

        if save_path:
            fig.savefig(save_path)
            logging.info(f"Plot saved to: {save_path}")
        else:
            fig.savefig(self.config['save_path'])
            logging.info(f"Plot saved to: {self.config['save_path']}") 
        
        if show_plot:
            plt.show()

        return fig  # Return the generated figure

    
    def notify_done(self, message: str = None) -> None:
        if not message:
            message = "Analysis is complete"
        
        try:
            ntfy_response = requests.post('https://ntfy.sh', data={'message': message, 'topic': self.config['ntfy_topic']})
            ntfy_response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info("Notification sent successfully")
        except requests.exceptions.RequestException as e:
            logging.warning(f'Unable to send notification: {e}')
