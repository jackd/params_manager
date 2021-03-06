"""Provides `ParamsManager` class for managing parameters folder."""
import os
import json


def _load(path):
    with open(path, 'r') as f:
        params = json.load(f)
    return params


def _save(path, params):
    with open(path, 'w') as f:
        json.dump(params, f)


class ParamsManager(object):
    """A class for managering parameter sets."""

    def __init__(self, folder, default_params=None, default_name=None):
        """
        Initialize the manager.

        Args:
            folder: folder under which this manager loads/saves parameters.
            default_params: default parameters. Can be None.
            default_name: name of default params file. Only used if
                default_params is None. Can be None.
        """
        self._folder = folder
        if default_params is None and default_name is not None:
            default_params = self.load(default_name)
        self._default_params = default_params

    @property
    def folder(self):
        """Get the model this manager looks for json files in."""
        return self._folder

    @property
    def default_params(self):
        """Get default parameters for this manager."""
        if self._default_params is None:
            return None
        return self._default_params.copy()

    def load(self, model_name):
        """Load parameters for the specified model."""
        path = self._path(model_name)
        if not os.path.isfile(path):
            raise IOError('No file at %s for model %s' % (path, model_name))
        else:
            return _load(path)

    def _path(self, model_name):
        return os.path.join(self._folder, '%s.json' % model_name)

    def set_params(self, model_name, params, overwrite=False):
        """
        Set parameters for the specified model.

        Values of `default_params` for keys not in `params` are entered into
        `params`.

        Returns True if no params were present for the given model.
        Returns False if params were present and were consistent.
        Raises IOError if parameters already existed and `overwrite` is False
        """
        if self._default_params is not None:
            for k in params:
                if k not in self._default_params:
                    raise Exception(
                        'key %s not in default_params keys. '
                        'Possible keys are %s' %
                        (k, str(list([k for k in self._default_params]))))
            for k in self._default_params:
                if k not in params:
                    params[k] = self._default_params[k]
        path = self._path(model_name)
        if os.path.isfile(path):
            old_params = _load(path)
            if old_params != params:
                if not overwrite:
                    raise Exception('params already exist and are different.')
                else:
                    _save(path, params)
            return False
        else:
            if not os.path.isdir(self._folder):
                os.makedirs(self._folder)
            _save(path, params)
            return True
