import json

from pipelines.plugin.base_plugin import BasePlugin
from pipelines.plugin.exceptions import PluginError


class StatusLogger(BasePlugin):
    hook_prefix = ''
    hooks = (
        'on_pipeline_start',
        'on_pipeline_finish',
    )

    def __init__(self, file_path=None):
        super(StatusLogger, self).__init__()

        if file_path:
            self.file_path = file_path

    @classmethod
    def from_dict(cls, conf_dict):
        if 'status_file' not in conf_dict:
            if not isinstance(conf_dict['status_file'], basestring):
                raise PluginError('File logger has invalid status_file parameter')

        return StatusLogger(conf_dict['status_file'])

    def on_pipeline_start(self, *args):
        self._write({'status': 'processing'})

    def on_pipeline_finish(self, *args):
        self._write({'status': 'success'})

    def _write(self, status):
        if self.file_path:
            with open(self.file_path, 'w+') as f:
                json.dump(status, f, indent=2)
        else:
            # Write to stdout
            print(json.dumps(status, indent=2))
